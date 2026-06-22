# 🚲 Velo — Germany & Europe Bike Trip 2026

Planning hub for Kian's cycling trip across Germany and elsewhere in Europe.

> **Trip window:** **Mon 22 June → ~Mon 13 July 2026** (~3 weeks / 22 days)
> **Origin:** Alberta, Canada (likely YYC Calgary or YEG Edmonton)
> **Destination:** Germany + neighbouring European countries, by bicycle
> **Traveller:** Canadian citizen

---

## 📑 What's in this folder

| File | What it covers |
|------|----------------|
| **[PACKING-LIST.md](./PACKING-LIST.md)** | The concrete, checkbox "don't-forget-anything" list — bike & components, bags, tools/spares, clothing, camp/sleep, electronics, documents, health/toiletries. This is the file to print and tick off. |
| **[ROUTES.md](./ROUTES.md)** | Route options for a 3-week ride (Danube / Rhine / Elbe / Romantic Road), with stages, difficulty, and how each connects to your flights. |
| **[DEEP-RESEARCH.md](./DEEP-RESEARCH.md)** | The full multi-axis dossier: entry/border rules (EES & ETIAS), flying with a bike, German train bike rules, weather, accommodation & camping law, money, connectivity, navigation, safety/theft, insurance, nutrition, comfort, daily-distance planning, and a pre-departure timeline. |

---

## ✅ Confirmed trip facts (from your own calendar & Slack)

- **Out-of-Office** is set on your Google Calendar from **2026-06-22 01:00** to **2026-07-14 01:00** (America/Edmonton). Your Slack `#out-of-office` note reads: *"OOO (cycling trip in Europe) June 22–July 13."*
- Your calendar's home time zone is **America/Edmonton**, and a Slack note ("WFH in Canada June 15–18") confirms you're departing from **Alberta**.
- You have **two YouTube channels**, both linked from your homepage: **[@kiankyars](https://www.youtube.com/@kiankyars)** ("Technical", channel ID `UCjIwowfXAbWRS3zrqGSmIYw`) and **[@kkyars](https://www.youtube.com/@kkyars)** ("Personal"). The bike-parts video is most likely on the **Personal** channel.
- Your personal site is **[kiankyars.github.io](https://kiankyars.github.io/)** (Home / [Now](https://kiankyars.github.io/now/) / [Blog](https://kiankyars.github.io/blog/) / [Build](https://kiankyars.github.io/build/) / [About](https://kiankyars.github.io/about/)), sourced from the public repo `kiankyars/kiankyars.github.io`. You also keep a private notes vault in `kiankyars/obsidian` (updated today).

## ⚠️ Honest note on sources (please read)

You asked me to watch your YouTube videos — especially the one about the **bike parts you bought** — and to mine the trip materials in this directory.

Two hard constraints in this environment shaped the result:

1. **The `velo` git repo was empty** (no commits) — there were no pre-existing transcripts, notes, or a plan to read here. These files are the first contents.
2. **Direct web/video access is blocked by the environment's network policy.** `WebFetch`, `curl`, and `yt-dlp` are all denied (every request returns HTTP 403), so I could **not** open the YouTube watch pages or pull the auto-captions/transcripts. The connected Google/Gmail/Slack/Notion accounts are your **work** workspace (`judgmentlabs.ai`) — they contain no personal YouTube uploads and no personal bike-parts order emails (the Gmail "purchases" category is empty for 2026). Only `WebSearch` (which returns summaries, not full pages) was available.

**What that means for the packing list:** I could not transcribe the exact parts shown in your video, so I did **not** invent them. Instead, the packing/parts list is a comprehensive, best-practice checklist built from authoritative cycling sources (REI, BIKEPACKING.com, Adventure Cycling, Tom's Bike Trip, EuroVelo, Deutsche Bahn, etc.) and tailored to your specific trip parameters. **Use the "Bike & components" section to tick off the parts you actually bought** and flag anything missing.

### Investigation log (everything I tried to reach the video/parts list)

I did not give up at the first blocker — here is the full trail, so you can see exactly where the wall is and how to get past it:

| Avenue | Result |
|--------|--------|
| Local `velo` repo | Empty (no commits) — no pre-existing plan/transcripts |
| Google Drive (search + recent) | Only work docs; one *metaphorical* "riding a bike" mention. No trip files |
| Gmail (bike retailers, purchases category, travel, YouTube notifications) | Work account only; **0** personal bike orders / video notifications |
| Google Calendar | Confirmed OOO dates + Alberta time zone; no itinerary detail |
| Notion / Slack (via search) | Confirmed the OOO note; no trip plan |
| `WebSearch` | Found both channels + your site, but **can't enumerate the small personal channel's individual videos** |
| `WebFetch` (YouTube, RSS feed, Invidious, Jina reader, even Wikipedia) | **HTTP 403 on every domain** — blanket egress block |
| `yt-dlp` / `curl` from shell | **403 on every domain** — same block |
| GitHub `search_repositories` | ✅ Worked — enumerated your 67 repos, found `obsidian`, `kiankyars.github.io`, `velo` |
| GitHub `get_file_contents` on `obsidian` / `kiankyars.github.io` | ❌ **Access denied** — session scope is locked to `kiankyars/velo` only |
| GitHub `search_code` across your repos | 0 results (private repos aren't indexed without scoped auth) |

**Conclusion:** the bike-parts video is audio/visual content on your Personal channel, and there is **no machine-readable path to it from this sandbox.** The most likely text version of your plan/gear list (your `obsidian` vault or `kiankyars.github.io`) is also outside my allowed repo scope.

### ✅ How to unblock deliverables (1) & (2) — pick any one

1. **Paste the bike-parts video URL + its transcript** (YouTube → "..." → *Show transcript* → copy) into the chat. I'll convert it into an exact parts list in minutes.
2. **Add `kiankyars/obsidian` and/or `kiankyars/kiankyars.github.io` to this session's GitHub repo scope.** Then I can read your own notes/plan directly and build the list from them.
3. **Paste the text of your `/now` page or trip-planning note.** I'll fold it in.

Until then, `PACKING-LIST.md` is the best-practice, trip-tailored checklist — accurate and genuinely useful, just not transcribed from your specific video.

---

*Last updated: 2026-06-22.*
