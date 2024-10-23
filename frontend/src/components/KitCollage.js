import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Row, Col } from 'antd';

import DisplayKit from './DisplayKit';

const KitCollage = ({ country, league_id, team_id, season, kitType }) => {

  // Define the filenames of the images
  const [kits, setKits] = useState([]);

  const headers = { 'Authorization': `Token ${sessionStorage.getItem('token')}` };

  useEffect(() => {
      axios.get(`http://localhost:8000/api/v1/kits/?country=${country}&league_id=${league_id}&team_id=${team_id}&season=${season}&kitType=${kitType}&number=9`, {
        headers: headers
      }) 
        .then(response => setKits(response.data))
        .catch(error => console.error('Error fetching kits:', error));
    }, []);


    return (
      <div className="display-kit-grid">
        <Row gutter={[16, 16]}>
          {kits.map((kit, index) => (
            <Col span={8} key={index}>
              <div className="kit-set">
                <DisplayKit kit_id={kit.id} />
              </div>
            </Col>
          ))}
        </Row>
      </div>
    );
  }
export default KitCollage;
  