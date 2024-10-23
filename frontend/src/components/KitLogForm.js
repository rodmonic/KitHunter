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
    setFormData({ ...formData, country, league:null, team:null, season:null, kitType:null }); // Update state
    fetchData(`http://localhost:8000/api/v1/leagues/?country=${country}`, setLeagues);
  };

  const handleLeagueChange = (league) => {
    form.setFieldsValue({ team: null, season: null, kitType: null }); // Reset dependent fields
    setFormData({ ...formData, league, team:null, season:null, kitType:null }); // Update state
    fetchData(`http://localhost:8000/api/v1/teams/?league_id=${league}`, setTeams);
  };

  const handleTeamChange = (team) => {
    form.setFieldsValue({ season: null, kitType: null }); // Reset dependent field
    setFormData({ ...formData, team, season:null, kitType:null }); // Update state
    fetchData(`http://localhost:8000/api/v1/kits/seasons/?team_id=${team}`, setSeasons);
  };

  const handleSeasonChange = (season) => {
    const team = form.getFieldValue('team'); // Get the selected team
    form.setFieldsValue({ kitType: null }); // Reset dependent field
    setFormData({ ...formData, season, kitType:null }); // Update state
    fetchData(`http://localhost:8000/api/v1/kits/kit_types/?team_id=${team}&season=${season}`, setKitTypes);
  };

  const handleKitTypeChange = (kitType) => {
    setFormData({ ...formData, kitType }); // Update state
  };

  const handleSubmit = () => {
    const values = form.getFieldsValue();
    console.log('Form submitted:', values);
  };


  // Reusable Form Select Component
  const FormSelect = ({ label, name, placeholder, options, onChange, rules }) => (
    <Form.Item label={label} name={name} rules={rules}>
      <Select
        style={{ width: '100%' }}
        placeholder={placeholder}
        onChange={onChange}
        allowClear
      >
        {options.map((option) => (
          // Handling the key and value for different data structures
          <Option
            key={option.id || option} // Use option.id if it exists, otherwise use option
            value={option.id || option} // Use option.id if it exists, otherwise use option
          >
            {option.league_name || option.name || option} {/* Display appropriate text */}
          </Option>
        ))}
      </Select>
    </Form.Item>
  );


  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <Form form={form} layout="vertical" onFinish={handleSubmit}>
        <Row gutter={16}>
          <Col span={12}>
            <FormSelect
              label="Country"
              name="country"
              placeholder="Select a Country"
              options={countries}
              onChange={handleCountryChange}
              rules={[{ required: true, message: 'Please select a country' }]}
            />
            <FormSelect
              label="League"
              name="league"
              placeholder="Select a League"
              options={leagues}
              onChange={handleLeagueChange}
              rules={[{ required: true, message: 'Please select a league' }]}
            />
            <FormSelect
              label="Team"
              name="team"
              placeholder="Select a Team"
              options={teams}
              onChange={handleTeamChange}
              rules={[{ required: true, message: 'Please select a team' }]}
            />
            <FormSelect
              label="Season"
              name="season"
              placeholder="Select a Season"
              options={seasons}
              onChange={handleSeasonChange}
              rules={[{ required: true, message: 'Please select a season' }]}
            />
            <FormSelect
              label="Kit Type"
              name="kitType"
              placeholder="Select a Kit Type"
              options={kitTypes}
              onChange={handleKitTypeChange}
              rules={[{ required: true, message: 'Please select a kit type' }]}
            />
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
