import "./layout.css";

const Layout = ({ title, children }) => {
    return (
        <div className = "pageDiv">
            <nav>
                <h3>Mixed Ability Play</h3>
                <div className = "links">
                    {title !== "home" && <a href = "/">Home</a>}
                    {title !== "settings" && <a href = "/settings">Settings</a>}
                    {title !== "help" && <a href = "/help">Help</a>}
                </div>
            </nav>
            <main className = "container">
                {children}
            </main>
        </div>
    );
}

export default Layout;