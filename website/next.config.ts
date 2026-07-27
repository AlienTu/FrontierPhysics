import path from "node:path";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  turbopack: {
    // The site reads task packages from the repository root at build time,
    // so the workspace root has to be pinned to this directory explicitly.
    root: path.resolve(__dirname),
  },
};

export default nextConfig;
