# 🔐 Clerk Integration Guide

> **Purpose:** Correct instructions for integrating Clerk into our React (Vite) application.

## Official Clerk + React (Vite) Setup

1. Install the Clerk React SDK: `npm install @clerk/clerk-react@latest`
2. Set `VITE_CLERK_PUBLISHABLE_KEY` in `.env.local`
3. Wrap app in `<ClerkProvider>` in `main.tsx`
4. Use Clerk's components: `<SignedIn>`, `<SignedOut>`, `<SignInButton>`, `<SignUpButton>`, `<UserButton>`

---

## Environment Variable

```bash
# .env.local (gitignored, real key here)
VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
```

> **Note:** The `VITE_` prefix is required for Vite to expose to client-side code.

---

## Code Examples

### main.tsx - Wrap with ClerkProvider

```typescript
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { ClerkProvider } from "@clerk/clerk-react";

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;
if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Clerk Publishable Key");
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/">
      <App />
    </ClerkProvider>
  </StrictMode>
);
```

### App.tsx - Using Clerk Components

```typescript
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/clerk-react";

export default function App() {
  return (
    <header>
      <SignedOut>
        <SignInButton />
        <SignUpButton />
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </header>
  );
}
```

---

## Critical Rules

### ✅ ALWAYS DO
- Use `@clerk/clerk-react@latest`
- Use `VITE_CLERK_PUBLISHABLE_KEY` as env variable name
- Place `<ClerkProvider>` in `main.tsx`
- Store real keys only in `.env.local` (gitignored)
- Use placeholders in code examples

### ❌ NEVER DO
- Use `frontendApi` instead of `publishableKey`
- Use old env names like `REACT_APP_CLERK_PUBLISHABLE_KEY`
- Place `<ClerkProvider>` deeper in component tree
- Commit real keys to git

---

## Auth Methods Enabled

- ✅ Google Sign-In
- ✅ GitHub Sign-In  
- ✅ Email/Password

---

## References

- [Clerk React Quickstart](https://clerk.com/docs/quickstarts/react)
- [Clerk Declarative Mode](https://clerk.com/docs/guides/development/declarative-mode)
