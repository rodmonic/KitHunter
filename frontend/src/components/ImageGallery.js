import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Col, Row } from 'antd';
import DisplayKit from './DisplayKit';


const ImageGallery = ({ season, team }) => {
  // State for each list
  const [kits, setKits] = useState([]);

  // token for authentication
  const token = sessionStorage.getItem('token');
  const headers = {
    'Authorization': `Token ${token}`
  }

  // Fetch kits when a season or team is selected
  useEffect(() => {
    let url = '';
    if (season && team) {
      url = `http://localhost:8000/api/v1/kits/${team}/${season}`;
    } else if (team) {
      url = `http://localhost:8000/api/v1/kits/${team}/`;
    } else {
      // If no team is selected, clear the kits array
      setKits([]);
      return; // Exit early
    }

    axios.get(url, {headers: headers})
      .then(response => setKits(response.data))
      .catch(error => console.error('Error fetching kits:', error));
  }, [season, team]);

  return (
    <div>
      {kits.length > 0 ? (
        <Row gutter={[16, 24]}> {/* Horizontal and vertical gutters */}
          {kits.map(kit => (
            <Col key={kit.id} xs={24} sm={12} md={8} lg={6}>
              <Card
                title={`${kit.season} - ${kit.kit_type}`}
                style={{
                  width: '100%', // Make card take the full width of the column
                }}
              >
                <DisplayKit
                kit_id = {kit.id}
                />
              </Card>
            </Col>
          ))}
        </Row>
      ) : (
        <p></p>
      )}
    </div>
  );
};

export default React.memo(ImageGallery);
