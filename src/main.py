import requests
import random
import json
import time
import statbotics

base_url = "https://www.thebluealliance.com/api/v3"
api_key = "XXXXXXXXXXXXXXXXXXXXX"
veterans = []
rookies = []
sb = statbotics.Statbotics()
output = open("output_data.txt", "w")

start = time.perf_counter()

def get_and_classify_teams():
    url = f"{base_url}/teams/2026/"
    for i in range(24):
        response = requests.get(url + str(i), headers={"X-TBA-Auth-Key": api_key})
        for team in response.json():
            if "Off-Season Demo Team" in team["nickname"]:
                continue
            if int(team["rookie_year"]) <= 2015:
                veterans.append(team)
            else:
                rookies.append(team)
    print(f"Veterans: {len(veterans)}")
    print(f"Rookies: {len(rookies)}")

def create_random_sample(lst, sample_size):
    return random.sample(lst, k=sample_size)

def veterans_rookies_collection():
	get_and_classify_teams()

	print(f"Data retrieval and classification completed at {time.perf_counter() - start:.2f} s")

	sampled_veterans = create_random_sample(veterans, 100)
	sampled_rookies = create_random_sample(rookies, 100)
	
	print(f"Random sampling completed at {time.perf_counter() - start:.2f} s")
	
	print("Veterans:", file=output)
	
	for i, veteran in enumerate(sampled_veterans):
		team_number = veteran['team_number']
		win_rate = sb.get_team_year(team_number, 2026)['record']['winrate']
		print(f"{team_number}\t{win_rate}", file=output)
		print(f"Processed veteran team {team_number} ({i + 1}/100)")
	 
	print("\nRookies:", file=output)
	
	for i, rookie in enumerate(sampled_rookies):
		team_number = rookie['team_number']
		win_rate = sb.get_team_year(team_number, 2026)['record']['winrate']
		print(f"{team_number}\t{win_rate}", file=output)
		print(f"Processed rookie team {team_number} ({i + 1}/100)")

event_list = []
matches_sample_epa = []
matches_sample_opr = []
epa_correct_count = 0
opr_correct_count = 0

def epa_opr_collection():
    event_list = requests.get(f"{base_url}/events/2026/simple", headers={"X-TBA-Auth-Key": api_key}).json()
    for event in event_list:
        if event["country"] == "Israel" or event["event_type"] < 0 or event["event_type"] > 5:
            continue
        print(f"{event['key']} at {time.perf_counter() - start:.2f} s.")
        matches = requests.get(f"{base_url}/event/{event['key']}/matches/simple", headers={"X-TBA-Auth-Key": api_key}).json()
        opr_sample = create_random_sample(matches, len(matches) // 40)
        epa_sample = create_random_sample(matches, len(matches) // 40)
        opr_correct_count = 0
        epa_correct_count = 0
        oprs = requests.get(f"{base_url}/event/{event['key']}/oprs", headers={"X-TBA-Auth-Key": api_key}).json()
        for match in opr_sample:
            blue_sum = 0
            red_sum = 0
            blue_score = match["alliances"]["blue"]["score"]
            red_score = match["alliances"]["red"]["score"]
            for blue in match["alliances"]["blue"]["team_keys"]:
                blue_sum += oprs["oprs"][blue]
            for red in match["alliances"]["red"]["team_keys"]:
                red_sum += oprs["oprs"][red]
        	if blue_score != red_score and ((blue_score > red_score) == (blue_sum > red_sum)):
    			opr_correct_count += 1
    		matches_sample_opr.append((match["key"], 'T' if blue_sum == red_sum else 'B' if blue_sum > red_sum else 'R', 'T' if blue_score == red_score else 'B' if blue_score > red_score else 'R'))
    	for match in epa_sample:
        	blue_sum = 0
        	red_sum = 0
        	blue_score = match["alliances"]["blue"]["score"]
        	red_score = match["alliances"]["red"]["score"]
        	for blue in match["alliances"]["blue"]["team_keys"]:
        		blue_sum += sb.get_team_year(int(blue[3:]), 2026)['epa']['total_points']['mean']
        	for red in match["alliances"]["red"]["team_keys"]:
        		red_sum += sb.get_team_year(int(red[3:]), 2026)['epa']['total_points']['mean']
        	if blue_score != red_score and ((blue_score > red_score) == (blue_sum > red_sum)):
        		epa_correct_count += 1
        	matches_sample_epa.append((match["key"], 'T' if blue_sum == red_sum else 'B' if blue_sum > red_sum else 'R', 'T' if blue_score == red_score else 'B' if blue_score > red_score else 'R'))
	print("OPR Predictions:", file=output)
	for tup in matches_sample_opr:
		print(f"{tup[0]}\t{tup[1]}\t{tup[2]}", file=output)
	print("", file=output)
	for tup in matches_sample_epa:
		print(f"{tup[0]}\t{tup[1]}\t{tup[2]}", file=output)
	print(f"Sampling completed at {time.perf_counter() - start:.2f} s.")
	print(f"EPA Accuracy: {epa_correct_count} / {len(matches_sample_epa)}")
	print(f"OPR Accuracy: {opr_correct_count} / {len(matches_sample_opr)}")

epa_opr_collection()

output.close()

print(f"Data collection completed at {time.perf_counter() - start:.2f} s. Check stats_data.txt for results.")

# current year epa: sb.get_team_year(team['team_number'], 2026)['epa']['total_points']['mean']
# current year win rate: sb.get_team_year(team['team_number'], 2026)['record']['winrate']

# print('\nSampled Veterans:')    
# for team in sampled_veterans:
#     print(team['nickname'])

# print('\nSampled Rookies:')
# for team in sampled_rookies:
#     print(team['nickname'])
