import React from 'react';
import Layout from '../components/layout';
import Accordion from '../components/accordion';

const Help = () => {
    return (
        <Layout title = "help">
            <h1>Help</h1>
            <hr/>
            <p>
                FAQ
                <Accordion title = "Maze Game" ClassName='Maze'>
                    
                </Accordion>
            </p>
        </Layout>
    )
}
export default Help;
