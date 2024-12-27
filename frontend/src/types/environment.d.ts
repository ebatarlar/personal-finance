declare namespace NodeJS {
  interface ProcessEnv {
    NEXTAUTH_URL: string;
    NEXTAUTH_URL_INTERNAL?: string;
    VERCEL_URL?: string;
    [key: string]: string | undefined;
  }
}

// Augment the process variable
declare var process: NodeJS.Process;
