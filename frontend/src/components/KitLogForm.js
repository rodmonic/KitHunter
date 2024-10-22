import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Form, Select, Button, Row, Col } from 'antd';
import KitCollage from './KitCollage';

const { Option } = Select;

const KitLogForm = () => {
  const [form] = Form.useForm();
  const [countries, setCountries] = useState([]);
  const [leagues, setLeagues] = useState([]);
  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);
  const [kitTypes, setKitTypes] = useState([]);
  
  // State to force component re-renders
  const [formData, setFormData] = useState({
    country: null,
    league: null,
    team: null,
    season: null,
    kitType: null,
  });

  const headers = { 'Authorization': `Token ${sessionStorage.getItem('token')}` };

  // Fetch data utility
  const fetchData = (url, setter) => {
    axios.get(url, { headers })
      .then(response => setter(response.data))
      .catch(error => console.error(`Error fetching data from ${url}:`, error));
  };

  // Fetch lists based on current selections
  useEffect(() => {
    fetchData('http://localhost:8000/api/v1/leagues/countries/', setCountries);
  }, []);

  const handleCountryChange = (country) => {
    form.setFieldsValue({ league: null, team: null, season: null, kitType: null }); // Reset dependent fields
    setFormData({ ...formData, country }); // Update state
    fetchData(`http://localhost:8000/api/v1/leagues/?country=${country}`, setLeagues);
  };

  const handleLeagueChange = (league) => {
    form.setFieldsValue({ team: null, season: null, kitType: null }); // Reset dependent fields
    setFormData({ ...formData, league }); // Update state
    fetchData(`http://localhost:8000/api/v1/teams/?league_id=${league}`, setTeams);
  };

  const handleTeamChange = (team) => {
    form.setFieldsValue({ season: null, kitType: null }); // Reset dependent field
    setFormData({ ...formData, team }); // Update state
    fetchData(`http://localhost:8000/api/v1/kits/seasons/?team_id=${team}`, setSeasons);
  };

  const handleSeasonChange = (season) => {
    const team = form.getFieldValue('team'); // Get the selected team
    form.setFieldsValue({ kitType: null }); // Reset dependent field
    setFormData({ ...formData, season }); // Update state
    fetchData(`http://localhost:8000/api/v1/kits/kit_types/?team_id=${team}&season=${season}`, setKitTypes);
  };

  const handleKitTypeChange = (kitType) => {
    setFormData({ ...formData, kitType }); // Update state
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
                style={{ width: '100%' }}
                placeholder="Select a league"
                onChange={handleLeagueChange}
                allowClear
              >
                {leagues.map((league) => (
                  <Option key={league.id} value={league.id}>{league.league_name}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item label="Team" name="team" rules={[{ required: true, message: 'Please select a team' }]}>
              <Select
                style={{ width: '100%' }}
                placeholder="Select a team"
                onChange={handleTeamChange}
                allowClear
              >
                {teams.map((team) => (
                  <Option key={team.id} value={team.id}>{team.name}</Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item label="Season" name="sesaon" rules={[{ required: true, message: 'Please select a season' }]}>
              <Select
                style={{ width: '100%' }}
                placeholder="Select a season"
                onChange={handleSeasonChange}
                allowClear
              >
                {seasons.map((season) => (
                  <Option key={season} value={season}>{season}</Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item label="Kit Type" name="kitType" rules={[{ required: true, message: 'Please select a Kit Type' }]}>
              <Select
                style={{ width: '100%' }}
                placeholder="Select a Kit Type"
                onChange={handleKitTypeChange}
                allowClear
              >
                {kitTypes.map((kitType) => (
                  <Option key={kitType} value={kitType}>{kitType}</Option>
                ))}
              </Select>
            </Form.Item>
            
          </Col>
          <Col span={12}>
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <KitCollage 
                key={`${formData.country}-${formData.league}-${formData.team}-${formData.season}-${formData.kitType}`}
                country={formData.country}
                league_id={formData.league}
                team_id={formData.team}
                season={formData.season}
                kitType={formData.kitType}
              />
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
