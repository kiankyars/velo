import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "europe-by-bicycle.pptx");
const RENDER_DIR = path.join(ROOT, "build", "rendered");

const C = {
  paper: "#F2EADD",
  paper2: "#E6DBC8",
  white: "#FCF8F1",
  ink: "#1B1A16",
  muted: "#6F695F",
  line: "#CFC1AB",
  red: "#B43B2D",
  orange: "#E26A2C",
  blue: "#41616A",
  green: "#3D5A4C",
  dark: "#181814",
  dark2: "#26251F",
};

const F = {
  display: "DIN Condensed",
  body: "Avenir Next",
  serif: "Georgia",
};

const A = {
  flight: path.join(ROOT, "assets/photos/departure-flight.jpg"),
  day1: path.join(ROOT, "assets/photos/day-01-karlsruhe.jpg"),
  canal: path.join(ROOT, "assets/photos/day-02-alsace-canal.jpg"),
  border: path.join(ROOT, "assets/photos/day-03-tri-border.jpg"),
  falls: path.join(ROOT, "assets/photos/day-04-rhine-falls.jpg"),
  lyon: path.join(ROOT, "assets/photos/day-08-lyon.jpg"),
  aunt: path.join(ROOT, "assets/photos/paris-aunt.jpg"),
  jeanLuc: path.join(ROOT, "assets/photos/drocourt-jean-luc.jpg"),
  vimy: path.join(ROOT, "assets/photos/vimy-group.jpg"),
  brugesCanal: path.join(ROOT, "assets/photos/bruges-canal.jpg"),
  brugesBike: path.join(ROOT, "assets/photos/bruges-bike.jpg"),
  finish: path.join(ROOT, "assets/photos/finish-night.jpg"),
  aftermath: path.join(ROOT, "assets/photos/next-day-aftermath.jpg"),
  family: path.join(ROOT, "assets/photos/family-next-day.jpg"),
  map: path.join(ROOT, "assets/frames/route-map.jpg"),
  bikeBox: path.join(ROOT, "assets/frames/bike-box.jpg"),
  furka: path.join(ROOT, "assets/frames/furka-pass.jpg"),
  phone: path.join(ROOT, "assets/frames/phone-fixed.jpg"),
  shop: path.join(ROOT, "assets/frames/giant-bike-shop.jpg"),
  cobbles: path.join(ROOT, "assets/frames/paris-roubaix-cobbles.jpg"),
  tunnel: path.join(ROOT, "assets/frames/antwerp-tunnel.jpg"),
  sunset: path.join(ROOT, "assets/frames/german-sunset.jpg"),
  cathedral: path.join(ROOT, "assets/frames/cologne-cathedral.jpg"),
  rhine: path.join(ROOT, "assets/frames/final-rhine.jpg"),
};

const IMAGE_BYTES = new Map(
  await Promise.all(
    Object.values(A).map(async (assetPath) => [assetPath, new Uint8Array(await fs.readFile(assetPath))]),
  ),
);

function rect(slide, left, top, width, height, fill, options = {}) {
  return slide.shapes.add({
    geometry: options.geometry ?? "rect",
    position: { left, top, width, height },
    fill,
    line: options.line ?? { style: "solid", fill: "none", width: 0 },
    ...(options.radius ? { borderRadius: options.radius } : {}),
    ...(options.shadow ? { shadow: options.shadow } : {}),
    ...(options.name ? { name: options.name } : {}),
  });
}

function line(slide, left, top, width, height, fill = C.line, weight = 2) {
  return slide.shapes.add({
    geometry: "line",
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill, width: weight },
  });
}

function textBox(slide, text, left, top, width, height, options = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left, top, width, height },
    fill: options.fill ?? "none",
    line: options.line ?? { style: "solid", fill: "none", width: 0 },
    ...(options.radius ? { borderRadius: options.radius } : {}),
    ...(options.name ? { name: options.name } : {}),
  });
  shape.text = text;
  shape.text.style = {
    fontSize: options.size ?? 22,
    typeface: options.font ?? F.body,
    color: options.color ?? C.ink,
    bold: options.bold ?? false,
    italic: options.italic ?? false,
    alignment: options.align ?? "left",
    verticalAlignment: options.valign ?? "top",
    autoFit: options.autoFit ?? "shrinkText",
    wrap: "square",
    lineSpacing: options.lineSpacing ?? 0.98,
    insets: options.insets ?? { top: 0, right: 0, bottom: 0, left: 0 },
  };
  return shape;
}

function image(slide, source, left, top, width, height, options = {}) {
  return slide.images.add({
    blob: IMAGE_BYTES.get(source),
    contentType: "image/jpeg",
    alt: options.alt ?? "Trip photograph",
    fit: options.fit ?? "cover",
    position: { left, top, width, height },
    ...(options.crop ? { crop: options.crop } : {}),
    ...(options.geometry ? { geometry: options.geometry } : {}),
    ...(options.radius ? { borderRadius: options.radius } : {}),
  });
}

function eyebrow(slide, value, color = C.red, rightText = "") {
  textBox(slide, value.toUpperCase(), 64, 34, 600, 24, {
    size: 15,
    font: F.body,
    bold: true,
    color,
  });
  if (rightText) {
    textBox(slide, rightText.toUpperCase(), 920, 34, 296, 24, {
      size: 15,
      font: F.body,
      bold: true,
      color: C.muted,
      align: "right",
    });
  }
  line(slide, 64, 68, 1152, 0, C.line, 1);
}

function footer(slide, index, text = "EUROPE BY BICYCLE") {
  textBox(slide, text, 64, 684, 700, 18, {
    size: 12,
    color: C.muted,
    bold: true,
  });
  textBox(slide, String(index).padStart(2, "0"), 1130, 682, 86, 20, {
    size: 14,
    font: F.display,
    color: C.muted,
    bold: true,
    align: "right",
  });
}

function note(slide, body, sources) {
  slide.speakerNotes.textFrame.setText(
    `${body.trim()}\n\n[Sources]\n${sources.map((s) => `- ${s}`).join("\n")}\n[/Sources]`,
  );
  slide.speakerNotes.setVisible(true);
}

function addStat(slide, value, label, left, top, width, accent = C.red) {
  textBox(slide, value, left, top, width, 72, {
    size: 58,
    font: F.display,
    color: accent,
    bold: true,
  });
  textBox(slide, label.toUpperCase(), left, top + 67, width, 40, {
    size: 15,
    color: C.muted,
    bold: true,
    lineSpacing: 0.9,
  });
}

async function writeBlob(outputPath, blob) {
  await fs.writeFile(outputPath, new Uint8Array(await blob.arrayBuffer()));
}

const presentation = Presentation.create({
  slideSize: { width: 1280, height: 720 },
});

// 01 — Open on the finish, not the departure.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.dark;
  rect(slide, 0, 0, 670, 720, C.dark);
  image(slide, A.finish, 670, 0, 610, 720, {
    alt: "Kian holding his bicycle overhead after finishing at night",
  });
  rect(slide, 642, 0, 42, 720, C.red);
  textBox(slide, "24 JUN → 10 JUL 2026", 70, 54, 500, 28, {
    size: 17,
    color: C.orange,
    bold: true,
  });
  textBox(slide, "EUROPE\nBY BICYCLE", 70, 118, 520, 260, {
    size: 76,
    font: F.display,
    color: C.white,
    bold: true,
    lineSpacing: 0.83,
  });
  textBox(slide, "14 riding days  /  7 countries  /  3,049.44 km", 72, 410, 520, 72, {
    size: 22,
    color: C.white,
    bold: true,
  });
  line(slide, 72, 500, 88, 0, C.orange, 5);
  textBox(slide, "This is the trip I actually rode, not the route I drew before leaving.", 72, 530, 500, 90, {
    size: 24,
    color: "#D9D2C7",
  });
  note(
    slide,
    `Open at the finish. The trip ran from June 24 to July 10, 2026: 17 elapsed days, 14 riding days, three rest or non-riding days, and seven countries. The audited riding distance is 3,049.438 km. The point of the talk is not that the original plan worked. It is that nearly every important part of the trip arrived after the plan broke.`,
    [
      `${ROOT}/sources/trip-chronology.txt`,
      `${ROOT}/assets/manifest.txt`,
      "https://www.youtube.com/watch?v=NWt_1sTojmA",
    ],
  );
}

// 02 — Establish the audited route and explain the competing totals.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "The whole loop", C.red, "17 elapsed days");
  rect(slide, 44, 92, 690, 554, C.white, { radius: 18, shadow: "shadow-sm" });
  image(slide, A.map, 66, 106, 646, 526, {
    alt: "Personal route map of the Western Europe bicycle loop",
    crop: { left: 0.23, top: 0, right: 0.32, bottom: 0 },
    fit: "cover",
  });
  rect(slide, 486, 470, 226, 162, C.dark, { radius: 10 });
  textBox(slide, "14 RIDING DAYS", 510, 496, 178, 28, { size: 21, font: F.display, color: C.orange, bold: true });
  textBox(slide, "3 REST DAYS", 510, 540, 178, 28, { size: 21, font: F.display, color: C.white, bold: true });
  textBox(slide, "THE PLAN\nAND THE RIDE", 780, 108, 420, 118, {
    size: 46,
    font: F.display,
    bold: true,
  });
  line(slide, 780, 244, 420, 0, C.line, 1);
  addStat(slide, "4,173", "km in the original GPX", 780, 278, 190, C.muted);
  addStat(slide, "3,049.44", "km actually ridden", 996, 278, 220, C.red);
  textBox(
    slide,
    "The vlog says 3,000. The map graphic says 3,100. The GPS, FIT and Strava audit resolves it to 3,049.438 km.",
    780,
    410,
    420,
    110,
    { size: 21, color: C.ink },
  );
  rect(slide, 780, 550, 420, 72, C.paper2, { radius: 12 });
  textBox(slide, "EXCLUDED: S-BAHN + BRIG→SION + GENEVA→VALSERHÔNE TRAINS", 800, 569, 380, 38, {
    size: 14,
    color: C.muted,
    bold: true,
    align: "center",
    valign: "middle",
  });
  footer(slide, 2);
  note(
    slide,
    `Explain the numbers before anyone has to wonder which total is real. The original route file was 4,173 km. The public summary rounded the ride to about 3,100 km and the titles rounded it to 3,000 km. A later audit of Strava activities, FIT and GPX files, and Photos timestamps established 3,049.438 km as the preferred riding total, with a plausible range of 3,040 to 3,061 km. The S-Bahn on June 24 and train segments on June 29 and June 30 are excluded.`,
    [
      "/Users/kian/Developer/vélo/strava-europe-trip-audit-2026.md",
      `${ROOT}/assets/frames/route-map.jpg`,
      "https://www.youtube.com/watch?v=NWt_1sTojmA&t=12s",
    ],
  );
}

// 03 — Make the uneven effort visible.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "Daily riding distance", C.red, "km / trains removed");
  textBox(slide, "THE SHAPE OF 3,049 KM", 64, 94, 700, 64, {
    size: 48,
    font: F.display,
    bold: true,
  });
  textBox(slide, "The last two bars are not a typo.", 64, 158, 520, 40, {
    size: 21,
    color: C.muted,
  });
  slide.charts.add("bar", {
    position: { left: 58, top: 214, width: 1160, height: 340 },
    categories: ["24", "25", "26", "27", "28", "29", "30", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    series: [
      {
        name: "Kilometres",
        values: [224.37, 157.57, 202.55, 278.06, 0, 135.6, 163.87, 140.66, 172.48, 274.98, 287.47, 0, 206.39, 0, 197.17, 337.84, 270.42],
        fill: C.red,
        points: [
          { idx: 4, fill: C.line },
          { idx: 11, fill: C.line },
          { idx: 13, fill: C.line },
          { idx: 15, fill: C.orange },
          { idx: 16, fill: C.orange },
        ],
      },
    ],
    hasLegend: false,
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 38 },
    chartFill: "none",
    chartLine: { style: "solid", fill: "none", width: 0 },
    plotAreaFill: "none",
    plotAreaLine: { style: "solid", fill: "none", width: 0 },
    xAxis: {
      textStyle: { fill: C.muted, fontSize: 15, bold: true },
      line: { style: "solid", fill: C.line, width: 1 },
      majorGridlines: null,
    },
    yAxis: {
      min: 0,
      max: 350,
      majorUnit: 50,
      numberFormatCode: "0",
      textStyle: { fill: C.muted, fontSize: 14 },
      line: { style: "solid", fill: "none", width: 0 },
      majorGridlines: { style: "solid", fill: C.line, width: 1 },
    },
  });
  textBox(slide, "JUNE", 72, 557, 460, 24, { size: 13, color: C.muted, bold: true });
  textBox(slide, "JULY", 542, 557, 660, 24, { size: 13, color: C.muted, bold: true });
  rect(slide, 64, 600, 1152, 58, C.dark, { radius: 12 });
  textBox(slide, "FINAL 2 DAYS", 88, 618, 170, 24, { size: 14, color: C.orange, bold: true });
  textBox(slide, "608.26 KM", 270, 608, 240, 38, { size: 31, font: F.display, color: C.white, bold: true });
  textBox(slide, "LONGEST DAY", 652, 618, 170, 24, { size: 14, color: C.orange, bold: true });
  textBox(slide, "337.84 KM", 832, 608, 250, 38, { size: 31, font: F.display, color: C.white, bold: true });
  footer(slide, 3);
  note(
    slide,
    `Walk across the chart chronologically. There are three zero-distance days: June 28, July 5, and July 7. July 1 is reconstructed because the activity itself is missing. The final two riding days total 608.26 km. July 9 is the longest day at 337.84 km.`,
    [
      "/Users/kian/Developer/vélo/strava-europe-trip-audit-2026.md",
      `${ROOT}/sources/trip-chronology.txt`,
    ],
  );
}

// 04 — The equipment warning before departure.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "23 June / Frankfurt", C.red, "the day before ride 1");
  image(slide, A.flight, 64, 104, 450, 232, { alt: "Flight display en route to Germany" });
  image(slide, A.bikeBox, 64, 354, 450, 254, { alt: "Bicycle being unpacked from its cardboard box" });
  rect(slide, 544, 104, 672, 504, C.white, { radius: 18, shadow: "shadow-sm" });
  textBox(slide, "BEFORE KILOMETRE ONE,\nTHE BIKE WAS ALREADY LOOSE", 590, 146, 580, 126, {
    size: 46,
    font: F.display,
    bold: true,
    lineSpacing: 0.9,
  });
  line(slide, 590, 292, 84, 0, C.red, 5);
  textBox(
    slide,
    "I unpacked the bike in 33°C heat, rebuilt it, added the wrong tubeless sealant, and watched the headset rotate loose on the test ride.",
    590,
    326,
    550,
    126,
    { size: 23 },
  );
  textBox(slide, "THE FIRST PLAN CHANGE", 590, 490, 220, 22, { size: 14, color: C.red, bold: true });
  textBox(slide, "Leave tomorrow morning instead.", 590, 522, 500, 42, { size: 28, font: F.serif, italic: true });
  footer(slide, 4);
  note(
    slide,
    `The trip effectively starts one day before the official riding log. I left Canada at 3 a.m., said an emotional goodbye, and flew with the bicycle in a cardboard box. In Frankfurt it was 33°C. The bicycle survived the flight, but after assembly the headset loosened and rotated during a nine-kilometre test ride. I tightened it without a torque wrench and delayed the departure to the next morning. The sealant added that day later made the puncture unrepairable.`,
    [
      `${ROOT}/transcripts/day-01.txt`,
      "https://www.youtube.com/watch?v=nRVeTv7W0VE&t=44s",
      "/Users/kian/Library/Mobile Documents/com~apple~CloudDocs/obsidian/notes/2026-06-22.md",
    ],
  );
}

// 05 — A first-day crisis with a twelve-hour hole in the footage.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.dark;
  image(slide, A.day1, 788, 0, 492, 720, { alt: "End-of-day selfie in Karlsruhe" });
  rect(slide, 0, 0, 804, 720, C.dark);
  textBox(slide, "24 JUN / RIDE 1", 64, 40, 360, 24, { size: 15, color: C.orange, bold: true });
  textBox(slide, "ONE PEDAL.\nFOUR BIKE SHOPS.\n224.37 KM.", 64, 104, 650, 210, {
    size: 58,
    font: F.display,
    color: C.white,
    bold: true,
    lineSpacing: 0.82,
  });
  textBox(slide, "The pedal stripped the crank in Frankfurt. I rode one-footed to a station, took the train to Mainz, and found the part at shop number four.", 66, 348, 650, 112, {
    size: 22,
    color: "#D9D2C7",
  });
  line(slide, 68, 510, 610, 0, "#5E5A50", 2);
  rect(slide, 68, 498, 14, 24, C.orange, { radius: 7 });
  rect(slide, 658, 498, 14, 24, C.orange, { radius: 7 });
  textBox(slide, "08:00", 68, 538, 120, 24, { size: 14, color: C.orange, bold: true });
  textBox(slide, "20:25", 568, 538, 104, 24, { size: 14, color: C.orange, bold: true, align: "right" });
  textBox(slide, "THE CAMERA GOES SILENT FOR 12 HOURS", 176, 535, 390, 28, {
    size: 16,
    color: C.white,
    bold: true,
    align: "center",
  });
  textBox(slide, "22:00 / Karlsruhe / chocolate milk described as heaven", 68, 614, 610, 28, {
    size: 17,
    color: "#938D82",
  });
  note(
    slide,
    `Day one nearly ended the trip. I left at 6:30 instead of 5:00 after losing the Polar charger. The headset was still loose. Then the pedal loosened until it destroyed the crank-arm threads. I pedalled with one foot to a station, took a train to Mainz, tried four bicycle shops, and considered returning to the house. The fourth shop had the rare part. The vlog has a twelve-hour hole because I recorded nothing between roughly 8 a.m. and 8:25 p.m. I still reached Karlsruhe and celebrated with bananas, milk, and chocolate milk.`,
    [
      `${ROOT}/transcripts/day-01.txt`,
      `${ROOT}/sources/trip-chronology.txt`,
      "https://www.youtube.com/watch?v=nRVeTv7W0VE&t=303s",
    ],
  );
}

// 06 — The fast, hot opening block and first cascade of losses.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "25–27 June / rides 2–4", C.red, "638.18 km in 3 days");
  textBox(slide, "HEAT, BORDERS, AND A DEAD PHONE", 64, 92, 920, 62, {
    size: 46,
    font: F.display,
    bold: true,
  });
  const cards = [
    { x: 64, img: A.canal, day: "25 JUN", km: "157.57 KM", copy: "UP TO 42°C\nRHINE → ALSACE" },
    { x: 448, img: A.border, day: "26 JUN", km: "202.55 KM", copy: "TRI-BORDER\nPASSPORT ALMOST LOST" },
    { x: 832, img: A.falls, day: "27 JUN", km: "278.06 KM", copy: "4 COUNTRIES\nTHUNDERSTORM" },
  ];
  for (const card of cards) {
    rect(slide, card.x, 182, 352, 430, C.white, { radius: 14, shadow: "shadow-sm" });
    image(slide, card.img, card.x, 182, 352, 242, { alt: card.copy, geometry: "roundRect", radius: 14 });
    textBox(slide, card.day, card.x + 22, 448, 132, 22, { size: 14, color: C.red, bold: true });
    textBox(slide, card.km, card.x + 170, 440, 158, 32, { size: 26, font: F.display, bold: true, align: "right" });
    textBox(slide, card.copy, card.x + 22, 496, 308, 70, { size: 20, bold: true, lineSpacing: 0.92 });
  }
  textBox(slide, "GERMANY → FRANCE → SWITZERLAND → AUSTRIA → LIECHTENSTEIN", 64, 638, 1120, 28, {
    size: 17,
    color: C.muted,
    bold: true,
    align: "center",
  });
  footer(slide, 6);
  note(
    slide,
    `The next three days compress the trip into heat and border crossings. June 25 reached roughly 42°C and ended in Alsace after I realized the Polar charger was gone. June 26 crossed the France-Germany-Switzerland tri-border and included a near-loss of the passport. June 27 went past Rhine Falls and through Germany, Switzerland, Austria, and Liechtenstein in one day. Near Danis, a thunderstorm soaked and disabled the main phone.`,
    [
      `${ROOT}/transcripts/day-02.txt`,
      `${ROOT}/transcripts/day-03.txt`,
      `${ROOT}/transcripts/day-04.txt`,
      `${ROOT}/sources/trip-chronology.txt`,
    ],
  );
}

// 07 — Physical high point, placed after an involuntary rest day.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.dark;
  image(slide, A.furka, 0, 0, 1280, 720, { alt: "Mountain switchbacks during the Furka Pass descent" });
  rect(slide, 0, 0, 566, 720, C.dark);
  rect(slide, 566, 0, 12, 720, C.orange);
  textBox(slide, "29 JUN / RIDE 5 / 135.60 KM", 62, 48, 430, 24, { size: 15, color: C.orange, bold: true });
  textBox(slide, "FURKA\n2,436 M", 62, 112, 430, 170, {
    size: 72,
    font: F.display,
    color: C.white,
    bold: true,
    lineSpacing: 0.82,
  });
  textBox(slide, "The rest day before it was not recovery. It was Sunday, everything was closed, and I was stranded in Danis with a dead phone.", 62, 334, 430, 120, {
    size: 22,
    color: "#D9D2C7",
  });
  line(slide, 62, 498, 80, 0, C.orange, 5);
  textBox(slide, "Oberalp first. Then 13 km and 890 m up Furka.", 62, 526, 430, 74, {
    size: 24,
    color: C.white,
    bold: true,
  });
  textBox(slide, "“Only looking forward.”", 62, 624, 430, 38, { size: 25, font: F.serif, italic: true, color: C.orange });
  note(
    slide,
    `June 28 was a forced rest day: it was Sunday, repair shops were closed, the phone was dead, and I remained in Danis. Jérôme and Marika helped make the day bearable. The next morning I crossed Oberalp Pass at roughly 2,000 metres and then climbed Furka Pass at 2,436 metres. The Furka climb was about 13 kilometres and 890 metres of elevation. In the vlog I made a deliberate emotional reset: only looking forward. A train from Brig to Sion is excluded from the riding total.`,
    [
      `${ROOT}/transcripts/day-05.txt`,
      `${ROOT}/assets/frames/furka-pass.jpg`,
      "https://www.youtube.com/watch?v=hHPp29eo9OI&t=387s",
      "/Users/kian/Developer/vélo/strava-europe-trip-audit-2026.md",
    ],
  );
}

// 08 — The low point is intentionally text-led because no useful image exists.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.dark;
  textBox(slide, "30 JUN / SION → GENEVA / 163.87 KM", 64, 42, 700, 24, { size: 15, color: C.orange, bold: true });
  textBox(slide, "GENEVA", 64, 106, 440, 86, { size: 72, font: F.display, color: C.white, bold: true });
  textBox(slide, "Two Airbnb cancellations.\nThe backup phone died.\nThe main phone was still broken.", 66, 220, 580, 154, {
    size: 31,
    font: F.display,
    color: "#D8D0C4",
    bold: true,
    lineSpacing: 0.92,
  });
  line(slide, 684, 72, 0, 568, "#4A4840", 2);
  textBox(slide, "For two hours I rode around the city trying to work out where to sleep. I panicked. I cried. The only open shops I found were inside the station.", 736, 110, 430, 166, {
    size: 23,
    color: C.white,
  });
  rect(slide, 736, 326, 430, 220, C.orange, { radius: 14 });
  textBox(slide, "ZAHRAN", 768, 354, 360, 42, { size: 35, font: F.display, color: C.dark, bold: true });
  textBox(slide, "A stranger at the station heard what happened and offered me his balcony for the night.", 768, 414, 350, 100, { size: 23, color: C.dark, bold: true });
  textBox(slide, "The next morning: masala, eggs, and a way forward.", 66, 542, 580, 70, { size: 23, font: F.serif, italic: true, color: C.orange });
  footer(slide, 8, "THE LOW POINT");
  note(
    slide,
    `This is the emotional low point. After Lake Geneva and Evian, two Airbnb reservations cancelled. The backup iPhone ran out of charge, the main phone screen was broken, and stores had closed. I spent about two hours circling Geneva, panicking and crying, before going to the station. Zahran approached, heard that I had nowhere to sleep, and invited me to travel with him and stay on his balcony. The next morning his family provided masala and eggs.`,
    [
      `${ROOT}/transcripts/day-06.txt`,
      `${ROOT}/transcripts/day-07.txt`,
      "https://www.youtube.com/watch?v=8nglV62Vr2o&t=111s",
      `${ROOT}/sources/trip-chronology.txt`,
    ],
  );
}

// 09 — The route is revised after the phone returns.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "1 July / ride 7", C.red, "140.66 km reconstructed");
  image(slide, A.map, 64, 102, 650, 520, {
    alt: "Route map showing the northern return through Paris and Belgium",
    crop: { left: 0.23, top: 0, right: 0.32, bottom: 0 },
    fit: "cover",
  });
  rect(slide, 486, 458, 228, 164, C.dark, { radius: 10 });
  textBox(slide, "ROUTE\nREWRITTEN", 510, 486, 180, 72, {
    size: 31,
    font: F.display,
    color: C.white,
    bold: true,
    lineSpacing: 0.86,
  });
  textBox(slide, "POINT NORTH", 510, 578, 180, 20, { size: 14, color: C.orange, bold: true });
  image(slide, A.phone, 760, 102, 456, 256, { alt: "Repaired iPhone held outside Carrefour" });
  textBox(slide, "THE ORIGINAL ROUTE\nWAS NOW IMPOSSIBLE", 760, 390, 456, 100, {
    size: 40,
    font: F.display,
    bold: true,
    lineSpacing: 0.9,
  });
  textBox(slide, "264 km/day remained, including the Italian Alps.", 760, 514, 456, 52, { size: 23, color: C.red, bold: true });
  textBox(slide, "The replacement screen cost €180. My cousin transferred the payment. I pointed north: Lyon → Paris → Belgium → Rhine.", 760, 576, 456, 76, {
    size: 18,
    color: C.muted,
  });
  footer(slide, 9);
  note(
    slide,
    `On July 1 a random repair kiosk inside a Carrefour replaced the iPhone 15 screen for 180 euros. Payment itself took hours because the credentials were on the broken phone, so my cousin in Germany transferred the money. With planning restored, I calculated that the original route would require 264 kilometres every remaining day, including major days in the Italian Alps. I rejected it and rerouted north through Lyon, Paris, Belgium, the Netherlands, and back down the Rhine. The July 1 distance is reconstructed because the Strava activity is missing.`,
    [
      `${ROOT}/transcripts/day-07.txt`,
      `${ROOT}/assets/frames/phone-fixed.jpg`,
      "https://www.youtube.com/watch?v=8nglV62Vr2o&t=521s",
      "/Users/kian/Developer/vélo/strava-europe-trip-audit-2026.md",
    ],
  );
}

// 10 — Another mechanical problem becomes a story about help.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "2 July / ride 8", C.red, "172.48 km");
  textBox(slide, "THE NEXT PROBLEM WAS A PUNCTURE", 64, 92, 780, 58, { size: 45, font: F.display, bold: true });
  image(slide, A.shop, 64, 184, 672, 378, { alt: "At the Giant bicycle shop after reaching it on a leaking tyre" });
  image(slide, A.lyon, 760, 184, 456, 256, { alt: "Kian in central Lyon after the repair" });
  rect(slide, 760, 464, 456, 98, C.dark, { radius: 12 });
  textBox(slide, "OLIVIER + ANTON", 788, 486, 210, 28, { size: 22, font: F.display, color: C.orange, bold: true });
  textBox(slide, "€50 tyre · labour + tools free", 788, 520, 380, 24, { size: 17, color: C.white, bold: true });
  const facts = [
    ["20 KM", "ridden while it leaked"],
    ["2 L", "water dumped to save weight"],
    ["2–4 KM", "between hand-pump stops"],
  ];
  facts.forEach(([value, label], index) => addStat(slide, value, label, 64 + index * 244, 580, 214, index === 2 ? C.orange : C.red));
  textBox(slide, "Then: Lyon, the Saône, and a bed beside the river.", 810, 604, 390, 46, { size: 20, font: F.serif, italic: true, color: C.muted });
  footer(slide, 10);
  note(
    slide,
    `The puncture probably began the prior day. The sealant would not close it, and the front tyre fell toward roughly ten PSI. I was about twenty kilometres from a Giant shop. I dumped two litres of water, leaned back to take weight off the front wheel, avoided turns, and stopped every few kilometres to pump. Olivier and Anton replaced the tyre; the incorrect sealant prevented a patch. They charged only the 50-euro part and gave the labour and tools for free. I continued through Lyon and along the Saône.`,
    [
      `${ROOT}/transcripts/day-08.txt`,
      `${ROOT}/assets/frames/giant-bike-shop.jpg`,
      "https://www.youtube.com/watch?v=Jw-WU-_shfY&t=339s",
      `${ROOT}/assets/photos/day-08-lyon.jpg`,
    ],
  );
}

// 11 — Two hard French days create the first major closing push.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.dark;
  image(slide, A.aunt, 760, 0, 520, 720, { alt: "Dinner with Kian's aunt after arriving in Paris" });
  rect(slide, 0, 0, 774, 720, C.dark);
  textBox(slide, "3–4 JUL / RIDES 9–10", 64, 42, 500, 24, { size: 15, color: C.orange, bold: true });
  textBox(slide, "562.45 KM\nTO PARIS", 64, 104, 600, 142, { size: 68, font: F.display, color: C.white, bold: true, lineSpacing: 0.84 });
  line(slide, 64, 282, 620, 0, "#4E4C44", 1);
  textBox(slide, "03 JUL", 64, 316, 112, 24, { size: 15, color: C.orange, bold: true });
  textBox(slide, "274.98 KM · FLEURVILLE → NEVERS", 196, 308, 480, 34, { size: 27, font: F.display, color: C.white, bold: true });
  textBox(slide, "Wasp sting. Nosebleed. Lost Croc elastic. Headwind. An 80 km/h road with no shoulder.", 196, 356, 480, 74, { size: 19, color: "#D5CEC3" });
  textBox(slide, "04 JUL", 64, 476, 112, 24, { size: 15, color: C.orange, bold: true });
  textBox(slide, "287.47 KM · NEVERS → PARIS", 196, 468, 480, 34, { size: 27, font: F.display, color: C.white, bold: true });
  textBox(slide, "Started hungry. Fontainebleau. Paris traffic. Apple Maps sent me to the wrong address. Arrived about 23:30.", 196, 516, 480, 92, { size: 19, color: "#D5CEC3" });
  textBox(slide, "Dinner was still waiting.", 64, 640, 620, 34, { size: 25, font: F.serif, italic: true, color: C.orange });
  note(
    slide,
    `This is the first deliberate closing push. July 3 covered 274.98 km from Fleurville to Nevers through a wasp sting, nosebleed, lost Croc elastic, headwind, and a high-speed road without a shoulder. July 4 covered 287.47 km to Paris after starting hungry, passing a nuclear plant and Fontainebleau, and negotiating Paris traffic. Apple Maps supplied the wrong address near the end. I reached my aunt's home around 11:30 p.m. Two days total: 562.45 km.`,
    [
      `${ROOT}/transcripts/day-10.txt`,
      `${ROOT}/transcripts/day-11.txt`,
      `${ROOT}/sources/trip-chronology.txt`,
      `${ROOT}/assets/photos/paris-aunt.jpg`,
    ],
  );
}

// 12 — Rest and relationships become explicit parts of the route.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "5–7 July", C.red, "206.39 km ridden");
  textBox(slide, "PARIS → DROCOURT → VIMY", 64, 92, 760, 56, { size: 46, font: F.display, bold: true });
  const photos = [
    { x: 64, src: A.aunt, label: "05 JUL / PARIS", copy: "Rest with my aunt" },
    { x: 448, src: A.jeanLuc, label: "06 JUL / DROCOURT", copy: "Dinner with Jean-Luc" },
    { x: 832, src: A.vimy, label: "07 JUL / VIMY", copy: "A non-riding day" },
  ];
  for (const p of photos) {
    image(slide, p.src, p.x, 182, 352, 350, { alt: p.copy });
    rect(slide, p.x, 532, 352, 92, C.dark);
    textBox(slide, p.label, p.x + 20, 550, 312, 22, { size: 14, color: C.orange, bold: true });
    textBox(slide, p.copy, p.x + 20, 580, 312, 28, { size: 20, color: C.white, bold: true });
  }
  textBox(slide, "War cemeteries, poppies, coal slag heaps, and two days in which the kilometres were not the main event.", 64, 644, 1120, 28, {
    size: 19,
    color: C.muted,
    align: "center",
  });
  footer(slide, 12);
  note(
    slide,
    `July 5 was a rest day in Paris. On July 6 my aunt sent me out with eggs, and I rode 206.39 km north to Drocourt through war cemeteries, poppies, and the coal-mining landscape before staying with Jean-Luc. July 7 was another non-riding day, including a visit to Vimy by car. These pauses matter because the trip was no longer simply an attempt to complete a preloaded line. It now included specific people and places I wanted to reach.`,
    [
      `${ROOT}/transcripts/day-09.txt`,
      `${ROOT}/sources/trip-chronology.txt`,
      `${ROOT}/assets/photos/paris-aunt.jpg`,
      `${ROOT}/assets/photos/drocourt-jean-luc.jpg`,
      `${ROOT}/assets/photos/vimy-group.jpg`,
    ],
  );
}

// 13 — The final commitment is made in Bruges.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "8 July / ride 12", C.red, "197.17 km");
  image(slide, A.brugesCanal, 64, 102, 336, 512, { alt: "Bruges canal at the end of ride 12" });
  image(slide, A.cobbles, 430, 102, 786, 260, { alt: "Paris-Roubaix cobbles on the route to Belgium" });
  image(slide, A.brugesBike, 430, 390, 318, 224, { alt: "Bicycle in Bruges before the final two-day push" });
  textBox(slide, "IN BRUGES, I CHOSE\nTWO DAYS INSTEAD OF THREE", 786, 398, 430, 96, {
    size: 37,
    font: F.display,
    bold: true,
    lineSpacing: 0.9,
  });
  textBox(slide, "About 600 km remained. Finishing earlier meant seeing family sooner.", 786, 516, 410, 70, { size: 21, color: C.muted });
  rect(slide, 786, 602, 286, 34, C.orange, { radius: 17 });
  textBox(slide, "CHAIN: “PURE BUTTER”", 806, 609, 246, 20, { size: 14, color: C.dark, bold: true, align: "center" });
  footer(slide, 13);
  note(
    slide,
    `Ride 12 went from Drocourt to Bruges. The day included Paris-Roubaix cobbles, Tournai, a punishing headwind, and the contrast of Ghent's bicycle infrastructure. After maintenance, the chain felt like pure butter. The audited 197.17 km includes a 16.06 km loop around Bruges. That evening, with roughly 600 km remaining, I chose to cover it in two days rather than three so I could see family sooner.`,
    [
      `${ROOT}/transcripts/day-12.txt`,
      `${ROOT}/assets/frames/paris-roubaix-cobbles.jpg`,
      "https://www.youtube.com/watch?v=PTFawKQFJoo&t=85s",
      `${ROOT}/assets/photos/bruges-canal.jpg`,
      "/Users/kian/Developer/vélo/strava-europe-trip-audit-2026.md",
    ],
  );
}

// 14 — Longest day.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.dark;
  textBox(slide, "9 JUL / RIDE 13 / BRUGES → COLOGNE", 64, 42, 700, 24, { size: 15, color: C.orange, bold: true });
  textBox(slide, "337.84", 64, 104, 520, 120, { size: 106, font: F.display, color: C.white, bold: true });
  textBox(slide, "KM", 486, 166, 90, 40, { size: 34, font: F.display, color: C.orange, bold: true });
  textBox(slide, "BEFORE 06:00 → 23:30", 70, 252, 450, 38, { size: 26, font: F.display, color: C.white, bold: true });
  line(slide, 64, 316, 500, 0, "#4D4B43", 1);
  textBox(slide, "Canadian cemetery\nSint-Anna tunnel, 31 m underground\nBelgium → Netherlands → Germany\nPhone flashlight after dark", 68, 352, 500, 174, {
    size: 24,
    color: "#D8D0C4",
    lineSpacing: 1.04,
  });
  textBox(slide, "Longest day I had ever ridden.", 68, 582, 500, 40, { size: 26, font: F.serif, italic: true, color: C.orange });
  image(slide, A.tunnel, 626, 0, 654, 360, { alt: "Cyclists inside the Sint-Anna tunnel below Antwerp" });
  image(slide, A.sunset, 626, 360, 654, 360, { alt: "Sunset on the final kilometres toward Cologne" });
  note(
    slide,
    `Ride 13 began before 6 a.m. in Bruges and ended around 11:30 p.m. in Cologne. I stopped at a Canadian war cemetery, entered Antwerp through the Sint-Anna pedestrian and bicycle tunnel 31 metres below the river, crossed briefly through the Netherlands, and returned to Germany. The final dark kilometres were on paths, but I had to hold the phone forward as a flashlight while riding. The audited distance is 337.84 km, the longest day of the trip.`,
    [
      `${ROOT}/transcripts/day-13.txt`,
      `${ROOT}/assets/frames/antwerp-tunnel.jpg`,
      "https://www.youtube.com/watch?v=jKRlZC1f514&t=145s",
      `${ROOT}/assets/frames/german-sunset.jpg`,
      "/Users/kian/Developer/vélo/strava-europe-trip-audit-2026.md",
    ],
  );
}

// 15 — The final day and family waiting at the end.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  eyebrow(slide, "10 July / ride 14", C.red, "the final day");
  textBox(slide, "270.42 KM HOME", 64, 92, 640, 58, { size: 50, font: F.display, bold: true });
  image(slide, A.cathedral, 64, 184, 364, 220, { alt: "Cologne Cathedral early on the final morning" });
  image(slide, A.rhine, 64, 426, 364, 204, { alt: "Final Rhine crossing toward Frankfurt" });
  image(slide, A.finish, 458, 92, 430, 538, { alt: "Kian holding the bicycle overhead after finishing" });
  rect(slide, 920, 92, 296, 538, C.dark, { radius: 16 });
  textBox(slide, "COLOGNE", 950, 128, 236, 28, { size: 17, color: C.orange, bold: true });
  textBox(slide, "Cathedral before the city woke.", 950, 168, 236, 70, { size: 22, color: C.white, bold: true });
  textBox(slide, "BONN + RHINE", 950, 280, 236, 28, { size: 17, color: C.orange, bold: true });
  textBox(slide, "Dead legs, familiar river, last crossing.", 950, 320, 236, 70, { size: 22, color: C.white, bold: true });
  textBox(slide, "AFTER 23:00", 950, 432, 236, 28, { size: 17, color: C.orange, bold: true });
  textBox(slide, "My family tracked the phone and waited in the driveway.", 950, 472, 236, 90, { size: 22, color: C.white, bold: true });
  textBox(slide, "608.26 KM / FINAL 2 DAYS", 950, 584, 236, 22, { size: 14, color: C.orange, bold: true, align: "center" });
  footer(slide, 15);
  note(
    slide,
    `The last day began in Cologne with the cathedral, continued through Bonn and along the Rhine, and ended after 11 p.m. in Mittelbuchen. The legs felt dead after the prior day's record, but the route was familiar again. My family tracked the phone and waited outside in the driveway. The final day was 270.42 km. Together, the last two days total 608.26 km.`,
    [
      `${ROOT}/transcripts/day-14.txt`,
      `${ROOT}/assets/frames/cologne-cathedral.jpg`,
      `${ROOT}/assets/frames/final-rhine.jpg`,
      `${ROOT}/assets/photos/finish-night.jpg`,
      "/Users/kian/Developer/vélo/strava-europe-trip-audit-2026.md",
    ],
  );
}

// 16 — Close on the exact daily-note line, then name the help concretely.
{
  const slide = presentation.slides.add();
  slide.background.fill = C.paper;
  image(slide, A.finish, 0, 0, 480, 720, { alt: "Finish portrait at night" });
  rect(slide, 480, 0, 16, 720, C.red);
  textBox(slide, "10 JUL 2026 / DAILY NOTE", 550, 48, 620, 24, { size: 15, color: C.red, bold: true });
  textBox(slide, "I LOVE LIFE\nSO MUCH", 550, 116, 650, 170, {
    size: 72,
    font: F.display,
    bold: true,
    lineSpacing: 0.82,
  });
  line(slide, 550, 322, 600, 0, C.line, 1);
  textBox(slide, "Zahran", 550, 358, 150, 28, { size: 22, font: F.display, color: C.red, bold: true });
  textBox(slide, "a balcony", 710, 358, 300, 28, { size: 20, color: C.muted });
  textBox(slide, "My cousin", 550, 404, 150, 28, { size: 22, font: F.display, color: C.red, bold: true });
  textBox(slide, "the €180 transfer", 710, 404, 300, 28, { size: 20, color: C.muted });
  textBox(slide, "Olivier + Anton", 550, 450, 150, 40, { size: 20, font: F.display, color: C.red, bold: true });
  textBox(slide, "the tyre, labour, and tools", 710, 450, 410, 30, { size: 20, color: C.muted });
  textBox(slide, "My aunt + Jean-Luc", 550, 504, 180, 36, { size: 20, font: F.display, color: C.red, bold: true });
  textBox(slide, "food, rooms, and time", 746, 504, 360, 30, { size: 20, color: C.muted });
  textBox(slide, "Family", 550, 554, 150, 28, { size: 22, font: F.display, color: C.red, bold: true });
  textBox(slide, "waiting in the driveway", 710, 554, 340, 28, { size: 20, color: C.muted });
  rect(slide, 550, 618, 610, 56, C.dark, { radius: 10 });
  textBox(slide, "17 DAYS LATER: BLISTERS, NUMB TOES, NECK PAIN. STILL WORTH IT.", 572, 635, 566, 24, {
    size: 15,
    color: C.white,
    bold: true,
    align: "center",
  });
  note(
    slide,
    `End on the exact line from the July 10 daily note: I LOVE LIFE SO MUCH. Do not turn it into a generic lesson. Name the people and the concrete acts that kept the trip moving: Zahran offered the balcony; my cousin transferred the phone payment; Olivier and Anton repaired the bicycle; my aunt and Jean-Luc supplied food and rooms; family waited in the driveway. Keep the physical cost in the ending too. Seventeen days later I still recorded hand blisters, numb toes, and neck pain.`,
    [
      "/Users/kian/Library/Mobile Documents/com~apple~CloudDocs/obsidian/notes/2026-07-10.md",
      "/Users/kian/Library/Mobile Documents/com~apple~CloudDocs/obsidian/notes/2026-07-11.md",
      `${ROOT}/research/story-notes.txt`,
      `${ROOT}/assets/photos/finish-night.jpg`,
    ],
  );
}

await fs.rm(RENDER_DIR, { recursive: true, force: true });
await fs.mkdir(RENDER_DIR, { recursive: true });

for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(path.join(RENDER_DIR, `${stem}.png`), await presentation.export({ slide, format: "png", scale: 1 }));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(RENDER_DIR, `${stem}.layout.json`), await layout.text());
}

await writeBlob(
  path.join(RENDER_DIR, "deck-montage.webp"),
  await presentation.export({ format: "webp", montage: true, scale: 1 }),
);

const deck = await PresentationFile.exportPptx(presentation);
await deck.save(OUT);
console.log(`Wrote ${OUT}`);
