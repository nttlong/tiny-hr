import React from 'react';

const GridComponent = ({ children, numColumns = 3 }) => {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: `repeat(${numColumns}, 1fr)` }}>
      {children}
    </div>
  );
};

export default GridComponent;