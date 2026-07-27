import path from "node:path";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // The site is served from a sub-path of benchflow.ai, not from a domain root.
  // Without this every asset and internal link resolves to `/` and the deployed
  // page renders unstyled. Set BASE_PATH="" to serve from a root instead.
  basePath: process.env.BASE_PATH ?? "/frontierphysics",
  turbopack: {
    // The site reads task packages from the repository root at build time,
    // so the workspace root has to be pinned to this directory explicitly.
    root: path.resolve(__dirname),
  },
};

export default nextConfig;
