# 📐 Coding Standards

We follow **Google Style Guides** for all code in this project.

---

## Style Guide References

| Language | Guide |
|----------|-------|
| **Python** | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) |
| **TypeScript** | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) |
| **HTML/CSS** | [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html) |

---

## Python Key Rules

- Use `snake_case` for functions, variables, modules
- Use `PascalCase` for classes
- Use `UPPER_SNAKE_CASE` for constants
- Maximum line length: 80 characters (preferred), 100 max
- Use type hints for all function signatures
- Write docstrings for all public modules, classes, functions
- Use `"""Google-style docstrings"""`

```python
def calculate_job_cost(
    job_id: str,
    execution_time: float,
) -> decimal.Decimal:
    """Calculate the cost of a completed job.

    Args:
        job_id: The unique identifier for the job.
        execution_time: Time in seconds the job ran.

    Returns:
        The calculated cost as a Decimal.

    Raises:
        ValueError: If job_id is not found.
    """
    ...
```

---

## TypeScript Key Rules

- Use `camelCase` for variables, functions, methods
- Use `PascalCase` for classes, interfaces, types, enums
- Use `UPPER_SNAKE_CASE` for constants
- Prefer `const` over `let`, never use `var`
- Use explicit types (avoid `any`)
- Use functional components for React

```typescript
interface JobResult {
  jobId: string;
  status: JobStatus;
  createdAt: Date;
}

const calculateJobCost = (jobId: string, executionTime: number): number => {
  // Implementation
};
```

---

## HTML/CSS Key Rules

- Use lowercase for HTML tags and attributes
- Use `kebab-case` for CSS class names
- Avoid inline styles
- Use semantic HTML (`<header>`, `<main>`, `<section>`)
- Use Tailwind utility classes (our CSS framework)

```html
<section class="job-results-container">
  <h2 class="text-xl font-bold">Results</h2>
</section>
```

---

## Tooling Enforcement

| Tool | Purpose |
|------|---------|
| **ruff** | Python linting (Google-style compatible) |
| **black** | Python formatting |
| **mypy** | Python type checking |
| **eslint** | TypeScript linting |
| **prettier** | TypeScript/CSS formatting |

---

## Commit to Quality

All code in this project will:
- ✅ Follow Google Style Guides
- ✅ Include type hints (Python) / explicit types (TypeScript)
- ✅ Have docstrings for public APIs
- ✅ Pass linting checks
- ✅ Be formatted consistently
