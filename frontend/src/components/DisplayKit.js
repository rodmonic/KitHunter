
import React from 'react';

const DisplayKit = ({ folder, height }) => {
// Define the filenames of the images
const images = ['Kit_left_arm.png', 'Kit_body.png',  'Kit_right_arm.png'];;

return (
    <div className="display-kit">
        <div  style={{ height: `${height}px` }}>
        {images.map((image, index) => (
            <img
            key={index}
            src={`${folder}/${image}`}
            alt={`Image ${index + 1}`}
            style={{ height: '100%' }} // Set the height to 100% to fill the container
            />
        ))}
        </div>
        <div>
            Kit Hunter
        </div>
    </div>
);
};

export default DisplayKit;
  