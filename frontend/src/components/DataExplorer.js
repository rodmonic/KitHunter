// DataExplorer.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Row, Col, List, Collapse } from 'antd';

const { Panel } = Collapse;

const DataExplorer = () => {
  // State for each list
  const [countries, setCountries] = useState([]);
  const [leagues, setLeagues] = useState([]);
  const [teams, setTeams] = useState([]);
  const [kits, setKits] = useState([]);

  // State for current selections
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);

  // Fetch the list of countries on mount
  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/countries/') // Adjust the endpoint to match your Django API
      .then(response => setCountries(response.data))
      .catch(error => console.error('Error fetching countries:', error));
  }, []);

  // Fetch leagues when a country is selected
  useEffect(() => {
    if (selectedCountry) {
      axios.get(`http://localhost:8000/api/v1/leagues/?country=${selectedCountry}`)
        .then(response => setLeagues(response.data))
        .catch(error => console.error('Error fetching leagues:', error));
    }
  }, [selectedCountry]);

  // Fetch teams when a league is selected
  useEffect(() => {
    if (selectedLeague) {
      axios.get(`http://localhost:8000/api/v1/teams/?league=${selectedLeague}`)
        .then(response => setTeams(response.data))
        .catch(error => console.error('Error fetching teams:', error));
    }
  }, [selectedLeague]);

  // Fetch kits when a team is selected
  useEffect(() => {
    if (selectedTeam) {
      axios.get(`http://localhost:8000/api/v1/kits/?team=${selectedTeam}`)
        .then(response => setKits(response.data))
        .catch(error => console.error('Error fetching kits:', error));
    }
  }, [selectedTeam]);

  return (
    <div>

      {/* Countries and Leagues */}
      <Row gutter={16}>
        <Col span={8}>
          <h2>Countries</h2>
          <List
            bordered
            dataSource={countries}
            renderItem={(country) => (
              <List.Item onClick={() => setSelectedCountry(
                country === selectedCountry ? null : country
                )}>
                {country}
              </List.Item>
            )}
          />
        </Col>
        {selectedCountry && (
          <Col span={8}>
            <h2>Leagues in {selectedCountry}</h2>
            <List
              bordered
              dataSource={leagues}
              renderItem={(league) => (
                <List.Item onClick={() => setSelectedLeague(league.id)}>
                  {league.league_name}
                </List.Item>
              )}
            />
          </Col>
        )}
      </Row>

      {/* Teams and Kits */}
      <Row gutter={16}>
        {selectedLeague && (
          <Col span={8}>
            <h2>Teams in {selectedLeague}</h2>
            <List
              bordered
              dataSource={teams}
              renderItem={(team) => (
                <List.Item onClick={() => setSelectedTeam(team.id)}>
                  {team.name}
                </List.Item>
              )}
            />
          </Col>
        )}
        {selectedTeam && (
          <Col span={8}>
            <h2>Kits for {selectedTeam}</h2>
            <Collapse defaultActiveKey={[]} accordion>
              {kits.map((kit, index) => (
                <Panel header={`Kit ${index + 1}`} key={index}>
                  <p>{kit}</p>
                </Panel>
              ))}
            </Collapse>
          </Col>
        )}
      </Row>
    </div>
  );
};

export default DataExplorer;
