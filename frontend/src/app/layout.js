import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Provider } from "react-redux"; // Redux provider that allows passing the store to the app
import { store } from "./redux/store";


// metadata to be used by Next.js for SEO and browser tab info
export const metadata = {
  title: "User Management",
  description: "A comrehensive user management system for manage users",
};

// The RootLayout component defines the root HTML structure for the application
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {/*allow all components to access the redux store*/}
        <Provider store={store}>
          {children}
        </Provider>

      </body>
    </html>
  );
}
