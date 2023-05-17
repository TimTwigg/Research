import React from 'react';
import Layout from '../components/layout';
import Accordion from '../components/accordion';

const Help = () => {
    return (
        <Layout title = "help">
            <h1>Help</h1>
            <div className='FAQ'>
                FAQ
                <Accordion title = "How do I assemble my Board?">
                    <p>
                    First, make sure the frame is assembled. <br />

                    Place the frame on top of the base. <br />

                    Then, place the board on top of the base. <br />

                    That's it lol
                    </p>
                </Accordion>
                <Accordion title = 'How do I use the camera?'>
                    <p>
                    First, make sure the camera is plugged in and any indicator light is on. <br />
                    Make sure the camera is selected in the dropdown menu. <br />
                    Click the "Enable Camera" button in the game menu. <br />
                    Allow the browser to access your camera when prompted. <br />
                    Make sure the camera has the entire board in frame. <br />
                    Click the "Take Image" button to take a picture of the board. <br />
                    </p>
                </Accordion>
            </div>
        </Layout>
    )
}
export default Help;
