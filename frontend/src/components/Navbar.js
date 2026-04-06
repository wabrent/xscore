import React from 'react';
import { Navbar as BsNavbar, Nav, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <BsNavbar bg="dark" variant="dark" className="navbar-custom">
      <Container>
        <BsNavbar.Brand as={Link} to="/dashboard">
          🚀 Crypto Twitter Tool
        </BsNavbar.Brand>
        <Nav className="me-auto">
          <Nav.Link as={Link} to="/dashboard">Дашборд</Nav.Link>
          <Nav.Link as={Link} to="/posts">Посты</Nav.Link>
          <Nav.Link as={Link} to="/crypto-trends">Крипто-тренды</Nav.Link>
          <Nav.Link as={Link} to="/analytics">Аналитика</Nav.Link>
        </Nav>
      </Container>
    </BsNavbar>
  );
};

export default Navbar;
