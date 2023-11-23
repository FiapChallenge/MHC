import Script from "next/script";
import { Metadata } from "next";
import Footer from "@/components/Footer/Footer";
import "./globals.css";
import "./styles/animation.css";
// @import url('https://fonts.googleapis.com/css?family=Anek Latin:700');
import { Poppins, Montserrat } from "next/font/google";
import Header from "@/components/Header/Header";
import RecoilContextProvider from "./recoilContextProvider";

const poppins = Poppins({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-poppins",
  weight: ["400", "700"],
});

const montserrat = Montserrat({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-montserrat",
  weight: ["400", "700"],
});

export const metadata: Metadata = {
  title: "Manchester HealthCare",
  description: "Manchester HealthCare",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-br" className={`${poppins.variable} ${montserrat.variable}`}>
      <body className={" scroll-top vsc-initialized font-body"}>
        <RecoilContextProvider>
          <Header />
          <main className="overflow-x-hidden">{children}</main>
          <Footer />
        </RecoilContextProvider>
      </body>
      <Script src="js/nav.js" />
      <Script src="js/scroll.js" />
    </html>
  );
}
