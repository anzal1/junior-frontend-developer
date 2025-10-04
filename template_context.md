# Template Conventions Guide

This guide outlines the specific file structure and coding conventions for the Vite + React + shadcn-ui template. You MUST follow these rules when generating plans and code.

## 1. Global CSS Import

The global stylesheet is located at `src/styles/globals.css`. It is **ONLY** imported once in the entire application, at the top of `src/main.tsx`.

**Correct:**

```tsx
// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./styles/globals.css"; // Correct way to import globals.css

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Incorrect:**
```tsx
// ❌ DO NOT import globals.css in components
import "./styles/globals.css"; // Wrong! Only import in main.tsx
```

## 2. Component Structure and Organization

### File Naming Conventions
- **Components**: Use PascalCase (e.g., `UserProfile.tsx`, `NavigationBar.tsx`)
- **Hooks**: Use camelCase with `use` prefix (e.g., `useAuth.ts`, `useLocalStorage.ts`)
- **Utils**: Use camelCase (e.g., `formatDate.ts`, `apiHelpers.ts`)
- **Types**: Use PascalCase with `.types.ts` suffix (e.g., `User.types.ts`)

### Directory Structure
```
src/
├── components/           # Reusable UI components
│   ├── ui/              # shadcn/ui components
│   ├── layout/          # Layout components (Header, Footer, Sidebar)
│   ├── forms/           # Form components
│   └── common/          # Other shared components
├── pages/               # Page components (if using routing)
├── hooks/               # Custom React hooks
├── utils/               # Utility functions
├── types/               # TypeScript type definitions
├── lib/                 # Library configurations
├── styles/              # CSS files
│   └── globals.css
└── assets/              # Static assets (images, icons)
```

### Component File Structure
```tsx
// ComponentName.tsx
import React from 'react';
import { cn } from '@/lib/utils';

interface ComponentNameProps {
  // Props interface
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  // destructured props
}) => {
  return (
    <div className={cn("base-classes", className)}>
      {/* Component content */}
    </div>
  );
};

export default ComponentName;
```

## 3. Import Conventions

### Import Order (CRITICAL - Follow this exact order):
1. **React and React-related imports**
2. **External library imports** (alphabetically)
3. **Internal imports using path alias `@/`**
4. **Relative imports** (same directory)
5. **Type-only imports** (using `import type`)

```tsx
// ✅ Correct import order
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { UserService } from '@/services/userService';
import { LocalComponent } from './LocalComponent';
import type { User } from '@/types/User.types';
```

### Path Aliases
Always use the `@/` alias for imports from the `src` directory:
```tsx
// ✅ Correct
import { Button } from '@/components/ui/button';
import { formatDate } from '@/utils/dateUtils';

// ❌ Incorrect
import { Button } from '../../../components/ui/button';
import { formatDate } from '../../utils/dateUtils';
```

## 4. shadcn/ui Integration

### Installing Components
When a shadcn/ui component is needed, install it using:
```bash
pnpm dlx shadcn@latest add [component-name]
```

### Component Usage
```tsx
// Always import shadcn components from @/components/ui/
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
```

### Customization
Customize shadcn components by:
1. **Using className prop** for styling adjustments
2. **Creating wrapper components** for consistent styling
3. **Using the `cn` utility** for conditional classes

```tsx
import { cn } from '@/lib/utils';

<Button 
  className={cn(
    "bg-primary hover:bg-primary/90",
    isLoading && "opacity-50 cursor-not-allowed"
  )}
>
  Click me
</Button>
```

## 5. Styling Guidelines

### Tailwind CSS Usage
- Use Tailwind utility classes for styling
- Follow mobile-first responsive design principles
- Use CSS custom properties for theme values

```tsx
// ✅ Good Tailwind usage
<div className="flex flex-col gap-4 p-6 md:flex-row md:gap-6 lg:p-8">
  <div className="flex-1 rounded-lg border bg-card p-4 shadow-sm">
    Content
  </div>
</div>
```

### CSS Variables (Design Tokens)
Use CSS custom properties defined in `globals.css`:
```css
/* Use these predefined theme variables */
.custom-element {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
  border-color: hsl(var(--border));
}
```

## 6. TypeScript Conventions

### Interface Definitions
```tsx
// Component props interfaces
interface UserProfileProps {
  user: User;
  isEditable?: boolean;
  onUpdate?: (user: User) => void;
}

// Use descriptive names ending with Props
interface NavigationBarProps {
  items: NavItem[];
  currentPath: string;
}
```

### Type Exports
```tsx
// Export types for reuse
export type { User, UserProfile } from './User.types';
export type { ApiResponse } from './Api.types';
```

## 7. State Management

### React Hooks Pattern
```tsx
const [state, setState] = useState<StateType>(initialState);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

// Custom hooks for complex logic
const { user, updateUser, isLoading } = useUser();
```

### Form Handling
Use controlled components with proper TypeScript typing:
```tsx
const [formData, setFormData] = useState<FormData>({
  name: '',
  email: '',
});

const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const { name, value } = e.target;
  setFormData(prev => ({
    ...prev,
    [name]: value
  }));
};
```

## 8. Error Handling

### Component Error Boundaries
```tsx
const [error, setError] = useState<Error | null>(null);

if (error) {
  return (
    <div className="rounded-lg border border-destructive/20 p-4">
      <h3 className="text-destructive">Something went wrong</h3>
      <p className="text-sm text-muted-foreground">{error.message}</p>
    </div>
  );
}
```

### API Error Handling
```tsx
try {
  const data = await fetchUserData();
  setUser(data);
} catch (error) {
  setError(error instanceof Error ? error.message : 'An error occurred');
} finally {
  setLoading(false);
}
```

## 9. Performance Best Practices

### Component Optimization
```tsx
// Use React.memo for expensive components
export const ExpensiveComponent = React.memo(({ data }: Props) => {
  return <div>{/* Expensive rendering logic */}</div>;
});

// Use useCallback for functions passed to children
const handleClick = useCallback(() => {
  // Handler logic
}, [dependency]);

// Use useMemo for expensive calculations
const expensiveValue = useMemo(() => {
  return heavyCalculation(data);
}, [data]);
```

### Lazy Loading
```tsx
// Code splitting with React.lazy
const LazyComponent = React.lazy(() => import('./LazyComponent'));

// Use with Suspense
<Suspense fallback={<div>Loading...</div>}>
  <LazyComponent />
</Suspense>
```

## 10. Accessibility Guidelines

### ARIA Attributes
```tsx
<button
  aria-label="Close dialog"
  aria-expanded={isOpen}
  aria-controls="dialog-content"
  onClick={handleClose}
>
  <CloseIcon aria-hidden="true" />
</button>
```

### Semantic HTML
```tsx
// Use semantic HTML elements
<nav aria-label="Main navigation">
  <ul role="list">
    <li><a href="/home">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <h1>Page Title</h1>
  <section aria-labelledby="section-title">
    <h2 id="section-title">Section Title</h2>
  </section>
</main>
```

## 11. Testing Conventions

### Component Testing Structure
```tsx
// ComponentName.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles user interactions', () => {
    const handleClick = jest.fn();
    render(<ComponentName onClick={handleClick} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## 12. Code Quality Rules

### ESLint and Prettier
Follow these rules:
- Use consistent indentation (2 spaces)
- Add trailing commas in multiline structures
- Use single quotes for strings
- No unused imports or variables
- Prefer const over let when possible

### Comments and Documentation
```tsx
/**
 * UserProfile component displays user information with edit capabilities
 * @param user - The user object containing profile data
 * @param isEditable - Whether the profile can be edited
 * @param onUpdate - Callback function called when user data is updated
 */
export const UserProfile: React.FC<UserProfileProps> = ({
  user,
  isEditable = false,
  onUpdate
}) => {
  // Component implementation
};
```

## 13. Environment and Configuration

### Environment Variables
```tsx
// Use proper typing for environment variables
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_TITLE: string;
}

// Usage
const apiUrl = import.meta.env.VITE_API_URL;
```

### Configuration Files
Keep `vite.config.ts`, `tailwind.config.js`, and `tsconfig.json` properly configured with path aliases and proper TypeScript settings.

## 14. Animation Guidelines

### Framer Motion Integration
```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>
```

### CSS Animations
Use Tailwind's animation utilities or CSS custom animations:
```tsx
<div className="animate-pulse">Loading...</div>
<div className="transition-all duration-200 hover:scale-105">
  Hover me
</div>
```

## Summary Checklist

When creating components, ensure:
- ✅ Global CSS is only imported in `main.tsx`
- ✅ Components follow proper naming conventions
- ✅ Imports are in the correct order
- ✅ Path aliases (`@/`) are used consistently
- ✅ shadcn/ui components are properly installed and imported
- ✅ TypeScript interfaces are properly defined
- ✅ Error handling is implemented
- ✅ Accessibility attributes are included
- ✅ Performance optimizations are considered
- ✅ Code follows quality standards
