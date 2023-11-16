import RootLayout from "./layout"

export default function App(children: React.ReactNode) {
    return (
        <RootLayout>
            {children}
        </RootLayout>
    )
}