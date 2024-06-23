import React from "react";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";

const Header = () => {
	return (
		<Navbar bg="dark" data-bs-theme="dark" className="py-3">
			<Container>
				<Navbar.Brand href="#home">
					<h4>Job Category Classification App</h4>
				</Navbar.Brand>
			</Container>
		</Navbar>
	);
};

export default Header;
