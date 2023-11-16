import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "@/styles/globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
    title: "Tactile Play",

}

export default function RootLayout({ children } : { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <div className = "pageDiv">
                    <nav>
                        <h3>Tactile Play</h3>
                        <div className = "links">
                            <a href = "/">Home</a>
                            <a href = "/settings">Settings</a>
                            <a href = "/help">Help</a>
                        </div>
                    </nav>
                    <main className = "container">
                        {children}
                    </main>
                </div>
            </body>
        </html>
    )
}
