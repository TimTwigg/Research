import React, { useState } from 'react';
import './accordion.css';

const Accordion = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="accordion">
      <div className="accordion-header" onClick={toggleAccordion}>
        <h2>{title}</h2>
        <span className={`icon ${isOpen ? 'open' : ''}`}></span>
      </div>
      {isOpen && (
        <div className="accordion-body">
          {children}
        </div>
      )}
    </div>
  );
};

export default Accordion;
