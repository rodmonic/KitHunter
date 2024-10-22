import React, { useState, useEffect } from 'react';
import axios from 'axios';

import DisplayKit from './DisplayKit';

const KitCollage = ({ country, league, team, season, kitType }) => {
// Define the filenames of the images
const [kits, setKits] = useState([]);

const headers = { 'Authorization': `Token ${sessionStorage.getItem('token')}` };

useEffect(() => {
    axios.get(`http://localhost:8000/api/v1/kits/?country=${country}&league=${league}&team=${team}&season=${season}&kitType=${kitType}`, {
      headers: headers
    }) 
      .then(response => setKits(response.data))
      .catch(error => console.error('Error fetching countries:', error));
  }, []);


return (
    <div className="display-kit">
      {kits.map((kit, index) =>(
      <DisplayKit
        kit_id={kit.id}
      />
      ))}
    </div>
);
};

export default KitCollage;
  