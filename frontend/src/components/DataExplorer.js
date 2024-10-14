  import React, { useState, useEffect } from 'react';
  import axios from 'axios';  // You can use fetch too, but axios simplifies API requests.
  
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
        axios.get(`http://localhost:8000/api/v1//teams/?league=${selectedLeague}`)
          .then(response => setTeams(response.data))
          .catch(error => console.error('Error fetching teams:', error));
      }
    }, [selectedLeague]);
  
    // Fetch kits when a team is selected
    useEffect(() => {
      if (selectedTeam) {
        axios.get(`http://localhost:8000/api/v1//kits/?team=${selectedTeam}`)
          .then(response => setKits(response.data))
          .catch(error => console.error('Error fetching kits:', error));
      }
    }, [selectedTeam]);
  
    return (
      <div>
        <h1>Data Explorer</h1>
  
        {/* Countries List */}
        <h2>Countries</h2>
        <ul>
          {countries.map((country, index) => (
            <li key={index} onClick={() => setSelectedCountry(country)}>
              {country}
            </li>
          ))}
        </ul>
  
        {/* Leagues List (only show if a country is selected) */}
        {selectedCountry && (
          <>
            <h2>Leagues in {selectedCountry}</h2>
            <ul>
              {leagues.map((league, index) => (
                <li key={index} onClick={() => setSelectedLeague(league)}>
                  {league.league_name}
                </li>
              ))}
            </ul>
          </>
        )}
  
        {/* Teams List (only show if a league is selected) */}
        {selectedLeague && (
          <>
            <h2>Teams in {selectedLeague}</h2>
            <ul>
              {teams.map((team, index) => (
                <li key={index} onClick={() => setSelectedTeam(team)}>
                  {team}
                </li>
              ))}
            </ul>
          </>
        )}
  
        {/* Kits List (only show if a team is selected) */}
        {selectedTeam && (
          <>
            <h2>Kits for {selectedTeam}</h2>
            <ul>
              {kits.map((kit, index) => (
                <li key={index}>{kit}</li>
              ))}
            </ul>
          </>
        )}
      </div>
    );
  };
  
  export default DataExplorer;
   