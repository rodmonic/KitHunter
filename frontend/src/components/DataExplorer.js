import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Row, Col, Select } from 'antd';
import ImageGallery from './ImageGallery';

const { Option } = Select;

const DataExplorer = () => {
  // State for lists and selections
  const [countries, setCountries] = useState([]);
  const [leagues, setLeagues] = useState([]);
  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);
  
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedSeason, setSelectedSeason] = useState(null);

  const headers = { 'Authorization': `Token ${sessionStorage.getItem('token')}` };

  // Fetch data utility
  const fetchData = (url, setter) => {
    axios.get(url, { headers })
      .then(response => setter(response.data))
      .catch(error => console.error(`Error fetching data from ${url}:`, error));
  };

  // Fetch lists based on current selections
  useEffect(() => fetchData('http://localhost:8000/api/v1/leagues/countries/', setCountries), []);
  useEffect(() => {
    if (selectedCountry) fetchData(`http://localhost:8000/api/v1/leagues/?country=${selectedCountry}`, setLeagues);
  }, [selectedCountry]);
  useEffect(() => {
    if (selectedLeague) fetchData(`http://localhost:8000/api/v1/teams/?league_id=${selectedLeague}`, setTeams);
  }, [selectedLeague]);
  useEffect(() => {
    if (selectedTeam) fetchData(`http://localhost:8000/api/v1/kits/seasons/?team_id=${selectedTeam}`, setSeasons);
  }, [selectedTeam]);

  // Common select change handler
  const handleSelectChange = (setter, resetters = []) => (value) => {
    setter(value);
    resetters.forEach(reset => reset(null));
  };

  return (
    <Row gutter={8} style={{ height: '100%' }}>
      {/* Left Column for Select Boxes */}
      <Col span={4} style={{ padding: '16px' }}>
        <Select
          style={{ width: '100%' }}
          placeholder="Select a Country"
          onChange={handleSelectChange(setSelectedCountry, [setSelectedLeague, setSelectedTeam, setSelectedSeason])}
          value={selectedCountry}
          allowClear
        >
          {countries.map((country, index) => (
            <Option key={index} value={country}>{country}</Option>
          ))}
        </Select>

        {selectedCountry && (
          <Select
            style={{ width: '100%', marginTop: '16px' }}
            placeholder="Select a League"
            onChange={handleSelectChange(setSelectedLeague, [setSelectedTeam, setSelectedSeason])}
            value={selectedLeague}
            allowClear
          >
            {leagues.map(league => (
              <Option key={league.id} value={league.id}>{league.league_name}</Option>
            ))}
          </Select>
        )}

        {selectedLeague && (
          <Select
            style={{ width: '100%', marginTop: '16px' }}
            placeholder="Select a Team"
            onChange={handleSelectChange(setSelectedTeam, [setSelectedSeason])}
            value={selectedTeam}
            allowClear
          >
            {teams.map(team => (
              <Option key={team.id} value={team.id}>{team.name}</Option>
            ))}
          </Select>
        )}

        {selectedTeam && (
          <Select
            style={{ width: '100%', marginTop: '16px' }}
            placeholder="Select a Season"
            onChange={setSelectedSeason}
            value={selectedSeason}
            allowClear
          >
            {seasons.map((season, index) => (
              <Option key={index} value={season}>{season}</Option>
            ))}
          </Select>
        )}
      </Col>

      {/* Right Column for Displaying Content */}
      <Col span={18} style={{ padding: '16px' }}>
        <h2>
          {selectedCountry}
          {selectedLeague && ` > ${leagues.find(l => l.id === selectedLeague)?.league_name}`}
          {selectedTeam && ` > ${teams.find(t => t.id === selectedTeam)?.name}`}
          {selectedSeason && ` > ${selectedSeason}`}
        </h2>
        <ImageGallery season={selectedSeason} team={selectedTeam} />
      </Col>
    </Row>
  );
};

export default DataExplorer;
