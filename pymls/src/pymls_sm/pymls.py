import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from pandas import json_normalize
import datetime

class pymls:
    clubs ={
            'atlanta': '11091',
            'austin': '15296',
            'charlotte': '16629',
            'chicago': '1207',
            'cincinnati': '11504',
            'colorado': '436',
            'columbus': '454',
            'dallas': '1903',
            'd.c.': '1326',
            'houston': '1897',
            'kansas city': '421',
            'la': '1230',
            'lafc': '11690',
            'miami': '14880',
            'minnesota':'6977',
            'montreal': '1616',
            'nashville': '15154',
            'new england': '928',
            'new york': '399',
            'new york city': '9668',
            'orlando': '6900',
            'philadelphia':'5513',
            'portland': '1581',
            'salt lake': '1899',
            'san jose':'1131',
            'seattle': '3500',
            'st. louis': '17012',
            'toronto': '2077',
            'vancouver': '1708',
            'all': 'all'
        }

    def __init__(self, year, club = 'all', competition='regular'):
        self.club = club.lower()
        self.year = year
        self.competition = competition.lower()
        self.club_code = self.clubs[self.club]
        self.competitions1 = {'regular':'-regular_season_player_season_stat_', 'playoffs': '-postseason_player_season_stat_', '-postseason':'-postseason_player_season_stat_'}
        self.competitions2 = {'regular':'regular_season_statistics', 'playoffs':'postseason_statistics', 'postseason':'postseason_statistics'}
        self.stat_string1 = f"{self.competitions1[self.competition]}{'goals'}"
        self.stat_string2 = f"{self.competitions2[self.competition]}"
    
    def mls_api(self, url):
        r = requests.get(url)
        df = pd.json_normalize(r.json(), max_level=1)
        return df

    def get_player_stats(self):
        
        if self.club == 'all':
            url = f'https://stats-api.mlssoccer.com/v1/players/seasons?&season_opta_id={self.year}&competition_opta_id=98&page_size=50&page=1&order_by={self.stat_string1}&include={self.stat_string2}&include=club&include=player&order_by=player_last_name'
        elif self.club != 'all':
            f'https://stats-api.mlssoccer.com/v1/players/seasons?&season_opta_id={self.year}&competition_opta_id=98&club_opta_id={self.club_code}&page_size=30&order_by={self.stat_string1}&include={self.stat_string2}&include=club&include=player&order_by=player_last_name'
        
        player_df = self.mls_api(url)

        player_df['season_year'] = self.year
        # Clean Dates
        player_df['join_date'] = player_df['join_date'].apply(lambda x: datetime.datetime.fromtimestamp((x//1000)) ).to_frame()
        # Clean leave date and ignore nans
        player_df['player.birth_date'] = player_df['player.birth_date'].apply(lambda x: datetime.datetime.fromtimestamp((x//1000)) ).to_frame()

        # Rename dataframe columns
        player_df.columns = player_df.columns.str.replace(r'player.', '')
        player_df.columns = player_df.columns.str.replace(r'regular_season_statistics.', '')  
        player_df.columns = player_df.columns.str.replace(r'postseason_statistics.', '')  

        # Remove un-needed dataframe columns
        player_df = player_df.drop(columns=[
            'index',
            'timestamp',
            'id',
            'club_season_id',
            'created',
            'updated',
            'known_name',
            'club.created',
            'club.updated'
        ])

        return player_df

    def get_club_stats(self):
        url = f"https://stats-api.mlssoccer.com/v1/clubs/seasons?&season_opta_id={self.year}&competition_opta_id=98&page_size=30&include={self.stat_string2}&include=club"

        team_df = self.mls_api(url)
        team_df['season_year'] = self.year

        # Clean dates
        team_df['club.created'] = team_df['club.created'].apply(lambda x: datetime.datetime.fromtimestamp((x//1000)) ).to_frame()

        # Clean column names
        team_df.columns = team_df.columns.str.replace(r'regular_season_statistics.', '')  
        team_df.columns = team_df.columns.str.replace(r'postseason_statistics.', '')  

        # Remove columns
        team_df = team_df.drop(columns=[
            'index',
            'season_id',
            'club.updated',
            'club.id',
            'venue_id'
        ])

        return team_df
        


        # Add in analytics like most accurate passes, best goal keepers, etc.
