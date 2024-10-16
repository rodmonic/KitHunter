import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Row, Col, Select } from 'antd';
import ImageGallery from './ImageGallery'

const { Option } = Select;

const DataExplorer = () => {
  // State for each list
  const [countries, setCountries] = useState([]);
  const [leagues, setLeagues] = useState([]);
  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);

  // State for current selections
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedSeason, setSelectedSeason] = useState(null);

  // token for authentication
  const token = sessionStorage.getItem('token');
  const headers = {
    'Authorization': `Token ${token}`
  }

  // Fetch the list of countries on mount
  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/leagues/countries/', {
      headers: headers
    }) 
      .then(response => setCountries(response.data))
      .catch(error => console.error('Error fetching countries:', error));
  }, []);

  // Fetch leagues when a country is selected
  useEffect(() => {
    if (selectedCountry) {
      axios.get(`http://localhost:8000/api/v1/leagues/?country=${selectedCountry}`, {
        headers: headers
      }) 
        .then(response => setLeagues(response.data))
        .catch(error => console.error('Error fetching leagues:', error));
    }
  }, [selectedCountry]);

  // Fetch teams when a league is selected
  useEffect(() => {
    if (selectedLeague) {
      axios.get(`http://localhost:8000/api/v1/teams/?league_id=${selectedLeague}`, {
        headers: headers
      }) 
        .then(response => setTeams(response.data))
        .catch(error => console.error('Error fetching teams:', error));
    }
  }, [selectedLeague]);

  // Fetch seasons when a team is selected
  useEffect(() => {
    if (selectedTeam) {
      axios.get(`http://localhost:8000/api/v1/kits/seasons/?team_id=${selectedTeam}`, {
        headers: headers
      }) 
        .then(response => setSeasons(response.data))
        .catch(error => console.error('Error fetching seasons:', error));
    }
  }, [selectedTeam]);

  return (
    <div>
    <div>
      {/* Countries, Leagues, Teams, and Kits */}
      <Row gutter={16}>
        <Col span={6}>
          <Select
            style={{ width: '100%' }}
            placeholder="Select a Country"
            onChange={(value) => {
              setSelectedCountry(value);
              setSelectedLeague(null);
              setSelectedTeam(null);
              setSelectedSeason(null);
            }}
            value={selectedCountry}
            allowClear
          >
            {countries.map((country, index) => (
              <Option key={index} value={country}>
                {country}
              </Option>
            ))}
          </Select>
        </Col>

        {selectedCountry && (
          <Col span={6}>
            <Select
              style={{ width: '100%' }}
              placeholder="Select a League"
              onChange={(value) =>
              {
                setSelectedLeague(value);
                setSelectedTeam(null);
                setSelectedSeason(null);
              }}
              value={selectedLeague}
              allowClear
            >
              {leagues.map((league) => (
                <Option key={league.id} value={league.id}>
                  {league.league_name}
                </Option>
              ))}
            </Select>
          </Col>
        )}

        {selectedLeague && (
          <Col span={6}>
            <Select
              style={{ width: '100%' }}
              placeholder="Select a Team"
              onChange={(value) =>               {
                setSelectedTeam(value);
                setSelectedSeason(null);
              }}
              value={selectedTeam}
              allowClear
            >
              {teams.map((team) => (
                <Option key={team.id} value={team.id}>
                  {team.name}
                </Option>
              ))}
            </Select>
          </Col>
        )}

        {selectedTeam && (
          <Col span={6}>
            <Select
              style={{ width: '100%' }}
              placeholder="Select a Season"
              onChange={(value) => setSelectedSeason(value)}
              value={selectedSeason} // Kits are displayed as a list and not selected in this dropdown
              allowClear
            >
              {seasons.map((season, index) => (
                <Option key={index} value={season}>
                  {season}
                </Option>
              ))}
            </Select>
          </Col>
        )}
      </Row>
      <Row gutter={16}>
        <h1>Kits</h1>
      </Row>
      <ImageGallery  
        season = {selectedSeason}
        team = {selectedTeam}
      />
    </div>
    </div>
  );
};

export default DataExplorer;
