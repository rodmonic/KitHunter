import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Row, Col } from 'antd';


const KitCollage = ({ country, league_id, team_id, season, kitType }) => {
  const [kits, setKits] = useState([]);
  const [kitParts, setKitParts] = useState([]);

  const headers = { 'Authorization': `Token ${sessionStorage.getItem('token')}` };

  useEffect(() => {
    // Step 1: Fetch kits based on parameters
    axios.get(`http://localhost:8000/api/v1/kits/?country=${country}&league_id=${league_id}&team_id=${team_id}&season=${season}&kitType=${kitType}&number=15`, {
      headers: headers
    })
    .then(response => {
      setKits(response.data);

      // Extract kit IDs for batch retrieval of KitParts
      const kitIds = response.data.map(kit => kit.id);

      // Step 2: Fetch KitParts using batch endpoint
      if (kitIds.length > 0) {
        axios.post(`http://localhost:8000/api/v1/kit_parts/batch/`, { kit_ids: kitIds }, { headers: headers })
          .then(response => {
            setKitParts(response.data)
          })
          .catch(error => console.error('Error fetching kit parts:', error));
      }
    })
    .catch(error => console.error('Error fetching kits:', error));
  }, [country, league_id, team_id, season, kitType]);

  return (
    <div className="display-kit-grid">
      <Row gutter={[16, 16]}>
        {
        kits.map((kit, index) => {
          const filteredKitParts = kitParts.filter(kitPart => kitPart.kit === kit.id);
          return (          
          <Col span={8} key={index}>
            <div className="kit-set">
              <div className="display-kit">
                  {filteredKitParts.map((kitPart, index) => (
                      <img
                      key={index}
                      src={`./images/${kitPart.image_name}`}
                      alt={`${index + 1}`}
                      style={{ 
                          backgroundColor: kitPart.background_color,
                      }} // Set the height to 100% to fill the container
                      />
                  ))
                  } 
              </div>
              
            </div>
          </Col>)
        }

        )}
      </Row>
    </div>
  );
};

export default KitCollage;
