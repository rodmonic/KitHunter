import React from 'react';

import DisplayKit from './DisplayKit'

const Header = () => {
  return (
    <header className="header">
      <h1>
        <DisplayKit folder ='' height= {40} />
        {/* Kit Hunter */}
      </h1>
    </header>
  );
};

export default Header;