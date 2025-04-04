import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DisplayKit = ({ kit_id, height }) => {
// Define the filenames of the images
const [images, setImages] = useState([]);

const headers = { 'Authorization': `Token ${sessionStorage.getItem('token')}` };

useEffect(() => {
    axios.get(`http://localhost:8000/api/v1/kit_parts/${kit_id}`, {
      headers: headers
    }) 
      .then(response => setImages(response.data))
      .catch(error => console.error('Error fetching countries:', error));
  }, [kit_id]);


return (
    <div className="display-kit">
        {images.map((image, index) => (
            <img
            key={index}
            src={`./images/${image.image_name}`}
            alt={`${index + 1}`}
            style={{ 
                height: '100%',
                backgroundColor: image.background_color,
                display: 'flex',
                flexDirection: 'row', // Ensures images are side by side
                justifyContent: 'space-around', // Adjust spacing as needed
                alignItems: 'center',
            }} // Set the height to 100% to fill the container
            />
        ))}
    </div>
);
};

export default DisplayKit;
  