import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Form, Select, Button, Row, Col } from 'antd';
// import KitCollage from './KitCollage';

const { Option } = Select;

const KitLogForm = () => {
  const [form] = Form.useForm(); // Create form instance
  const [countries, setCountries] = useState([]);
  const [leagues, setLeagues] = useState([]);
  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);
  const [kitTypes, setKitTypes] = useState([]);
  
  const headers = { 'Authorization': `Token ${sessionStorage.getItem('token')}` };

  // Fetch data utility
  const fetchData = (url, setter) => {
    axios.get(url, { headers })
      .then(response => setter(response.data))
      .catch(error => console.error(`Error fetching data from ${url}:`, error));
  };

  // Fetch lists based on current selections
  useEffect(() => fetchData('http://localhost:8000/api/v1/leagues/countries/', setCountries), []);

  const handleCountryChange = (country) => {
    form.setFieldsValue({ league: null, team: null, season: null, type: null }); // Reset dependent fields
    fetchData(`http://localhost:8000/api/v1/leagues/?country=${country}`, setLeagues);
  };

  const handleLeagueChange = (league) => {
    form.setFieldsValue({ team: null, season: null, type: null }); // Reset dependent fields
    fetchData(`http://localhost:8000/api/v1/teams/?league_id=${league}`, setTeams);
  };

  const handleTeamChange = (team) => {
    form.setFieldsValue({ season: null, type: null }); // Reset dependent field
    fetchData(`http://localhost:8000/api/v1/kits/seasons/?team_id=${team}`, setSeasons);
  };

  const handleSeasonChange = (season) => {
    const team = form.getFieldValue('team'); // Get the selected team
    form.setFieldsValue({ type: null }); // Reset dependent field
    fetchData(`http://localhost:8000/api/v1/kits/kit_types/?team_id=${team}&season=${season}`, setKitTypes);
  };


  const handleSubmit = () => {
    const values = form.getFieldsValue();
    console.log('Form submitted:', values);
  };

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <Form form={form} layout="vertical" onFinish={handleSubmit}>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item label="Country" name="country" rules={[{ required: true, message: 'Please select a country' }]}>
              <Select
                style={{ width: '100%' }}
                placeholder="Select a Country"
                onChange={handleCountryChange}
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
                onChange={handleLeagueChange}
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
                onChange={handleTeamChange}
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
                onChange={handleSeasonChange}
                allowClear
              >
                {seasons.map((season, index) => (
                  <Option key={index} value={season}>{season}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item label="Type" name="type" rules={[{ required: true, message: 'Please select a kit type' }]}>
            <Select
                style={{ width: '100%', marginTop: '16px' }}
                placeholder="Select a Kit Type"
                allowClear
              >
                {kitTypes.map((kitType, index) => (  // Use kitTypes instead of seasons
                  <Option key={index} value={kitType}>{kitType}</Option>  // Adjust according to your data structure
                ))}
              </Select>
            </Form.Item>
          </Col>
          <Col span={12}>
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {/* <KitCollage 
                country={form.getFieldValue('country')}
                league={form.getFieldValue('league')}
                team={form.getFieldValue('team')}
                season={form.getFieldValue('season')}
                kitType={form.getFieldValue('kitType')}
                 /> */}
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
