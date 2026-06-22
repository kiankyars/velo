#!/usr/bin/env python3
import os
import sys
import json
import re
import math
from datetime import datetime
import xml.etree.ElementTree as ET

# Paths
BASE_DIR = "/Users/kian/Developer/vélo"
CONFIG_PATH = os.path.join(BASE_DIR, "trip_config.json")
TODO_PATH = os.path.join(BASE_DIR, "todo.md")
GPX_DIR = os.path.join(BASE_DIR, "gpx")

# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: {CONFIG_PATH} not found.")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0)**2
        
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def parse_gpx(gpx_path):
    try:
        tree = ET.parse(gpx_path)
        root = tree.getroot()
        
        # Namespaces are common in GPX files
        ns = ""
        m = re.match(r'({.*})', root.tag)
        if m:
            ns = m.group(1)
            
        points = []
        elevations = []
        
        # Traverse GPX points
        for trkpt in root.findall(f'.//{ns}trkpt'):
            lat = float(trkpt.attrib['lat'])
            lon = float(trkpt.attrib['lon'])
            points.append((lat, lon))
            
            ele = trkpt.find(f'{ns}ele')
            if ele is not None and ele.text:
                elevations.append(float(ele.text))
                
        # Calculate distance
        total_distance = 0.0
        for i in range(len(points) - 1):
            total_distance += haversine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
            
        # Calculate elevation gain (sum of positive changes)
        elevation_gain = 0.0
        for i in range(len(elevations) - 1):
            diff = elevations[i+1] - elevations[i]
            if diff > 0:
                elevation_gain += diff
                
        return {
            "distance_km": total_distance,
            "elevation_gain_m": elevation_gain,
            "points_count": len(points)
        }
    except Exception as e:
        return {"error": str(e)}

def cmd_status():
    config = load_config()
    print(f"\n{BOLD}{CYAN}=== {config['trip_name']} Status ==={RESET}")
    
    # Calculate countdowns
    today = datetime.now().date()
    dates = config["dates"]
    
    def print_countdown(label, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        diff = (date_obj - today).days
        if diff > 0:
            print(f"🗓️  {label}: {BOLD}{date_str}{RESET} ({YELLOW}{diff} days to go{RESET})")
        elif diff == 0:
            print(f"🗓️  {label}: {BOLD}{date_str}{RESET} ({GREEN}Today!{RESET})")
        else:
            print(f"🗓️  {label}: {BOLD}{date_str}{RESET} ({BLUE}{-diff} days ago{RESET})")
            
    print_countdown("Edmonton Departure", dates["edmonton_departure"])
    print_countdown("Europe Departure", dates["europe_departure"])
    print_countdown("Europe Return", dates["europe_return"])
    
    print(f"\n{BOLD}✈️  Flight Bookings:{RESET}")
    for flight in config["flights"]:
        status_color = GREEN if flight["status"] == "booked" else YELLOW
        print(f"  - [{status_color}{flight['status'].upper()}{RESET}] {flight['airline']}: {flight['route']} on {flight['date']}")
        
    print(f"\n{BOLD}🗺️  Planned Segments:{RESET}")
    for idx, r in enumerate(config["routes"]):
        print(f"  {idx+1}. {BOLD}{r['name']} ({r['ev_code']}){RESET}: {r['start']} -> {r['end']} (~{r['approx_distance_km']} km)")

def cmd_todo():
    if not os.path.exists(TODO_PATH):
        print(f"Error: {TODO_PATH} not found.")
        sys.exit(1)
        
    with open(TODO_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    print(f"\n{BOLD}{CYAN}=== Trip Todos ==={RESET}")
    current_category = ""
    
    todo_count = 0
    done_count = 0
    
    for line in lines:
        line = line.strip()
        if line.startswith("## "):
            current_category = line[3:]
            print(f"\n{BOLD}{BLUE}{current_category}{RESET}")
        elif line.startswith("- `[ ]`"):
            todo_count += 1
            task_text = line.replace("- `[ ]`", "").strip()
            # Highlight key bold prefixes
            task_text = re.sub(r'\*\*(.*?)\*\*', f'{BOLD}\\1{RESET}', task_text)
            print(f"  [{YELLOW} {RESET}] {task_text}")
        elif line.startswith("- `[x]`"):
            done_count += 1
            task_text = line.replace("- `[x]`", "").strip()
            task_text = re.sub(r'\*\*(.*?)\*\*', f'{BOLD}\\1{RESET}', task_text)
            print(f"  [{GREEN}✓{RESET}] {task_text}")
            
    total = todo_count + done_count
    percentage = (done_count / total * 100) if total > 0 else 0
    print(f"\nProgress: {BOLD}{done_count}/{total} completed ({percentage:.1f}%){RESET}\n")

def cmd_check(search_term):
    if not os.path.exists(TODO_PATH):
        print(f"Error: {TODO_PATH} not found.")
        sys.exit(1)
        
    with open(TODO_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    updated = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith("- `[ ]`") and search_term.lower() in line.lower():
            # Found task!
            line = line.replace("`[ ]`", "`[x]`")
            task_text = line.strip().replace("- `[x]`", "").strip()
            print(f"Checked off: {GREEN}{task_text}{RESET}")
            updated = True
        new_lines.append(line)
        
    if updated:
        with open(TODO_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    else:
        print(f"No matching open task found containing: '{search_term}'")

def cmd_routes():
    print(f"\n{BOLD}{CYAN}=== Route Analysis ==={RESET}")
    gpx_files = [f for f in os.listdir(GPX_DIR) if f.endswith(".gpx")]
    
    if not gpx_files:
        print(f"No GPX files found in {GPX_DIR}/.")
        print("Add your EuroVelo GPX segment files to analyze them.")
        return
        
    total_dist = 0.0
    total_ele = 0.0
    
    for f_name in gpx_files:
        path = os.path.join(GPX_DIR, f_name)
        stats = parse_gpx(path)
        
        if "error" in stats:
            print(f"❌ {BOLD}{f_name}{RESET}: Error parsing ({stats['error']})")
        else:
            print(f"📌 {BOLD}{f_name}{RESET}:")
            print(f"   Distance: {BOLD}{stats['distance_km']:.2f} km{RESET}")
            print(f"   Elevation Gain: {BOLD}{stats['elevation_gain_m']:.1f} m{RESET}")
            print(f"   GPS Trackpoints: {stats['points_count']}")
            total_dist += stats['distance_km']
            total_ele += stats['elevation_gain_m']
            
    print(f"\n{BOLD}Total Route Metrics:{RESET}")
    print(f"  🏁 Distance: {BOLD}{total_dist:.2f} km{RESET}")
    print(f"  🏔️ Elevation Gain: {BOLD}{total_ele:.1f} m{RESET}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/planner.py [status|todo|check <term>|routes]")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "status":
        cmd_status()
    elif cmd == "todo":
        cmd_todo()
    elif cmd == "check":
        if len(sys.argv) < 3:
            print("Error: Specify a term to check off.")
            sys.exit(1)
        cmd_check(" ".join(sys.argv[2:]))
    elif cmd == "routes":
        cmd_routes()
    else:
        print(f"Unknown command: {cmd}")
        print("Available commands: status, todo, check <term>, routes")
        sys.exit(1)

if __name__ == "__main__":
    main()
