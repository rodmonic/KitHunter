import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Form, Select, Button, Row, Col, Image } from 'antd';
import DisplayKit from './DisplayKit';

const { Option } = Select;

const KitLogForm = () => {
  const [formData, setFormData] = useState({
    country: '',
    league: '',
    team: '',
    season: '',
    type: '',
  });

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

  const handleSubmit = () => {
    // Logic to handle form submission, e.g., sending data to an API
    console.log('Form submitted:', formData);
  };



  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <Form layout="vertical" onFinish={handleSubmit}>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item label="Country" name="country" rules={[{ required: true, message: 'Please select a country' }]}>
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
            </Form.Item>
            <Form.Item label="League" name="league" rules={[{ required: true, message: 'Please select a league' }]}>
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
            </Form.Item>
            <Form.Item label="Team" name="team" rules={[{ required: true, message: 'Please select a team' }]}>
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

            </Form.Item>
            <Form.Item label="Season" name="season" rules={[{ required: true, message: 'Please select a season' }]}>
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
            </Form.Item>
            <Form.Item label="Type" name="type" rules={[{ required: true, message: 'Please select a type' }]}>
      
            </Form.Item>
          </Col>
          <Col span={12}>
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
             <DisplayKit 
                  kit_id = "253"/>
              
            </div>
          </Col>
        </Row>
        <Row gutter={16} style={{ marginTop: 16 }}>
          <Col span={24}>
            <Button type="primary" htmlType="submit" style={{ width: '100%' }}>
              Submit
            </Button>
          </Col>
        </Row>
      </Form>
    </div>
  );
};

export default KitLogForm;
