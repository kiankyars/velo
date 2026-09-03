import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const captionsDir = path.join(root, "sources", "captions");
const metadataDir = path.join(root, "sources", "metadata");
const transcriptsDir = path.join(root, "transcripts");

function formatTimestamp(milliseconds) {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  if (hours > 0) {
    return [hours, minutes, seconds]
      .map((part) => String(part).padStart(2, "0"))
      .join(":");
  }

  return [minutes, seconds]
    .map((part) => String(part).padStart(2, "0"))
    .join(":");
}

function outputName(title) {
  const match = title.match(/\|\s*(Day\s+\d+|Summary)$/i);
  if (!match) {
    throw new Error(`Cannot derive transcript name from title: ${title}`);
  }

  const label = match[1].toLowerCase();
  if (label === "summary") return "summary.txt";

  const day = Number(label.match(/\d+/)[0]);
  return `day-${String(day).padStart(2, "0")}.txt`;
}

function captionText(event) {
  if (!event.segs) return "";
  return event.segs
    .map((segment) => segment.utf8 ?? "")
    .join("")
    .replace(/\s+/g, " ")
    .trim();
}

function groupSegments(segments) {
  const groups = [];
  let current = null;

  const flush = () => {
    if (!current) return;
    groups.push({
      startMs: current.startMs,
      text: current.parts.join(" ").replace(/\s+/g, " ").trim(),
    });
    current = null;
  };

  for (const segment of segments) {
    if (!current) {
      current = { startMs: segment.startMs, parts: [] };
    }

    current.parts.push(segment.text);
    const elapsedMs = segment.startMs - current.startMs;
    const closesSentence = /[.!?]["']?$/.test(segment.text);

    if ((elapsedMs >= 12_000 && closesSentence) || elapsedMs >= 18_000) {
      flush();
    }
  }

  flush();
  return groups;
}

fs.mkdirSync(transcriptsDir, { recursive: true });

const metadataFiles = fs
  .readdirSync(metadataDir)
  .filter((file) => file.endsWith(".info.json"));

const manifest = [];

for (const metadataFile of metadataFiles) {
  const metadataPath = path.join(metadataDir, metadataFile);
  const metadata = JSON.parse(fs.readFileSync(metadataPath, "utf8"));
  const captionFile = fs
    .readdirSync(captionsDir)
    .find((file) => file.includes(`[${metadata.id}]`) && file.endsWith(".json3"));

  if (!captionFile) {
    throw new Error(`Missing caption file for ${metadata.id}`);
  }

  const captions = JSON.parse(
    fs.readFileSync(path.join(captionsDir, captionFile), "utf8"),
  );
  const segments = captions.events
    .map((event) => ({
      startMs: event.tStartMs ?? 0,
      text: captionText(event),
    }))
    .filter((segment) => segment.text);

  const transcriptFile = outputName(metadata.title);
  const header = [
    metadata.title,
    `Video: ${metadata.webpage_url}`,
    `Video ID: ${metadata.id}`,
    `Duration: ${formatTimestamp(metadata.duration * 1000)}`,
    `Published: ${metadata.upload_date}`,
    "Caption source: YouTube automatic captions (en-orig); wording is uncorrected.",
    "",
  ];
  const lines = groupSegments(segments).map(
    (segment) => `[${formatTimestamp(segment.startMs)}] ${segment.text}`,
  );

  fs.writeFileSync(
    path.join(transcriptsDir, transcriptFile),
    `${[...header, ...lines].join("\n")}\n`,
  );

  manifest.push({
    day:
      transcriptFile === "summary.txt"
        ? null
        : Number(transcriptFile.match(/\d+/)[0]),
    title: metadata.title,
    videoId: metadata.id,
    url: metadata.webpage_url,
    durationSeconds: metadata.duration,
    published: metadata.upload_date,
    transcript: `transcripts/${transcriptFile}`,
    sourceCaption: `sources/captions/${captionFile}`,
    sourceMetadata: `sources/metadata/${metadataFile}`,
  });
}

manifest.sort((a, b) => {
  if (a.day === null) return 1;
  if (b.day === null) return -1;
  return a.day - b.day;
});

fs.writeFileSync(
  path.join(transcriptsDir, "manifest.json"),
  `${JSON.stringify(manifest, null, 2)}\n`,
);

console.log(`Wrote ${manifest.length} transcripts to ${transcriptsDir}`);
