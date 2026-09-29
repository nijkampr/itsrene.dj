// IT'S RENÉ · trailer capture. Steps render(t) frame by frame in headless
// Chromium and pipes the frames into ffmpeg with the soundtrack.
//
//   node trailer/capture.mjs                      -> trailer/build/itsrene-trailer.mp4
//   node trailer/capture.mjs --stills 3.2 17 44   -> trailer/build/still-*.png
//   add --reel to either for the 1080x1920 Instagram cut (itsrene-trailer-reel.mp4, reel-*.png)
//
// Needs: a static server on :8000 at the repo root (python3 -m http.server 8000),
// playwright (global), and an ffmpeg with libx264 (FFMPEG env var, or on PATH).
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT || "playwright");
const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "build");
const FPS = 30, DUR = 59;
const REEL = process.argv.includes("--reel");
const args = process.argv.slice(2).filter(a => a !== "--reel");
const [VW, VH] = REEL ? [1080, 1920] : [1920, 1080];
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ args: ["--force-color-profile=srgb"] });
const page = await browser.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
page.on("console", m => m.type() === "error" && console.error("page:", m.text()));
page.on("pageerror", e => console.error("page error:", e.message));
await page.goto(`http://localhost:8000/trailer/trailer.html?capture${REEL ? "&format=reel" : ""}`, { waitUntil: "load" });
await page.evaluate(() => window.ready);

const frame = (t, type) => page.evaluate(([t, type]) => {
  window.render(t);
  return document.getElementById("c").toDataURL(type, 0.96).split(",")[1];
}, [t, type]);

if (args[0] === "--stills") {
  for (const s of args.slice(1)) {
    writeFileSync(join(OUT, `${REEL ? "reel" : "still"}-${s}.png`), Buffer.from(await frame(+s, "image/png"), "base64"));
  }
  console.log(`${args.length - 1} stills -> ${OUT}`);
} else {
  const out = join(OUT, REEL ? "itsrene-trailer-reel.mp4" : "itsrene-trailer.mp4");
  const ff = spawn(process.env.FFMPEG || "ffmpeg", [
    "-y", "-loglevel", "error",
    "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-",
    "-i", join(OUT, "soundtrack.wav"),
    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-tune", "grain", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out,
  ], { stdio: ["pipe", "inherit", "inherit"] });
  const n = FPS * DUR, t0 = Date.now();
  for (let i = 0; i < n; i++) {
    const buf = Buffer.from(await frame(i / FPS, "image/png"), "base64");
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    if (i % 150 === 0) console.log(`frame ${i}/${n} · ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise((ok, no) => ff.on("close", c => c ? no(new Error("ffmpeg " + c)) : ok()));
  console.log("->", out);
}
await browser.close();
