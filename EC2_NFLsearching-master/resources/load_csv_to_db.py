"""
Run this file to insert data to sql table, make modification to suit the se
"""

import csv
import mysql.connector


# define MySQL connection parameters (modfify)
db_config = {
    "host": "c6156-nfl-searching-query-microservice-db.ckoq7q2zprcp.us-east-2.rds.amazonaws.com",
    "user": "tw6156",
    "password": "linguine_falafel_pita",
    "database": "dbNFLstat",
}

# # file location (modify) - this is for loading the player_basic_csv
# with open("C:/Users/15529/OneDrive/桌面/NFL_sample_data/player_basic_csv.csv",'r') as file:
#
#     reader = csv.reader(file)
#
#     connection = mysql.connector.connect(**db_config)
#
#     cursor = connection.cursor()
#
#     for row in reader:
#         cursor.execute('INSERT INTO player_basic_info (contract_id,player_id,name,draft_year,rnd,pick,tm,pos,game_played,year_signed,signing_tm,value,gtd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',row)
#
#     connection.commit()
#
# cursor.close()
#
# connection.close()


# # file location (modify) - this is for loading the weekly_data_updated_08_23.csv
# with open("C:/Users/15529/OneDrive/桌面/NFL_sample_data/weekly_data_updated_08_23.csv",'r') as file:
#
#     reader = csv.reader(file)
#
#     connection = mysql.connector.connect(**db_config)
#
#     cursor = connection.cursor()
#
#     for row in reader:
#         cursor.execute(
#             'INSERT INTO player_stat (event_id, player_id, name, position, team, week, season, season_type, completions, attempts, passing_yards, passing_tds, interceptions, sacks, sack_yards, sack_fumbles, sack_fumbles_lost, passing_air_yards, passing_yards_after_catch, passing_first_downs, passing_2pt_conversions, carries, rushing_yards, rushing_tds, rushing_fumbles, rushing_fumbles_lost, rushing_first_downs, rushing_2pt_conversions, receptions, targets, receiving_yards, receiving_tds, receiving_fumbles, receiving_fumbles_lost, receiving_air_yards, receiving_yards_after_catch, receiving_first_downs, receiving_2pt_conversions, target_share, air_yards_share, fantasy_points, fantasy_points_ppr, total_yards, ypa, ypc, ypr, touches, count, comp_percentage, pass_td_percentage, int_percentage, rush_td_percentage, rec_td_percentage, total_tds, td_percentage, passer_rating, rookie_season, round, overall, ht, wt, forty, vertical, offense_snaps, teams_offense_snaps, snap_pct, years_played) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
#             row)
#
#         print("data inserted")
#
#     connection.commit()
#
# cursor.close()
#
# connection.close()



# file location (modify) - this is for loading the weekly_data_updated_08_23.csv
with open("C:/Users/15529/OneDrive/桌面/NFL_sample_data/player_basic.csv",'r') as file:

    reader = csv.reader(file)

    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor()

    for row in reader:
        cursor.execute(
            'INSERT INTO player_basic (player_id, name, position, number, current_Team, height, weight, age, college) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            row)

        print("data inserted")

    connection.commit()

cursor.close()

connection.close()