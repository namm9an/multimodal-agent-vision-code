# 🧪 Testing Strategy & Error Handling

## Testing Philosophy
- **Test early, test often** - Catch issues before production
- **User-first error handling** - Always notify users before auto-remediation
- **Fail gracefully** - Degrade functionality, don't crash
- **Comprehensive coverage** - Unit → Integration → E2E

---

## 📊 Testing Pyramid

```
         /\
        /E2E\         5% - Critical user flows
       /------\
      /Integration\   25% - Service interactions  
     /------------\
    /     Unit     \  70% - Business logic
   /________________\
```

---

## 🎯 Test Coverage Requirements

### MVP Requirements
- **Unit Tests:** ≥80% coverage
- **Integration Tests:** Critical paths covered
- **E2E Tests:** 5 core user journeys
- **Security Tests:** Sandbox escape prevention
- **Critic Agent Tests:** Code validation accuracy

### What Must Be Tested
1. **Authentication & Authorization**
2. **Image upload validation** (PNG/JPG only)
3. **Agent reasoning logic**
4. **Code generation safety** (Python only)
5. **Critic agent** (ruff + bandit validation)
6. **Sandbox isolation** (Python only)
7. **Error recovery flows**

---

## 🔬 Unit Tests

### Backend Unit Tests

```python
# tests/unit/test_job_service.py
import pytest
from app.services.job_service import JobService
from app.models.job import JobStatus

class TestJobService:
    @pytest.fixture
    def job_service(self, mock_db):
        return JobService(db=mock_db)
    
    def test_create_job_success(self, job_service):
        """Test successful job creation"""
        job = job_service.create_job(
            user_id="test_user",
            file_path="test.png"
        )
        assert job.status == JobStatus.PENDING
        assert job.user_id == "test_user"
    
    def test_create_job_invalid_file(self, job_service):
        """Test job creation with invalid file type"""
        with pytest.raises(ValueError) as exc:
            job_service.create_job(
                user_id="test_user",
                file_path="test.pdf"  # PDF not supported in MVP
            )
        assert "Invalid file type" in str(exc.value)
    
    def test_create_job_image_only(self, job_service):
        """Test that only images are accepted"""
        valid_types = ["test.png", "test.jpg", "test.jpeg", "test.gif", "test.webp"]
        for file_path in valid_types:
            job = job_service.create_job(user_id="test_user", file_path=file_path)
            assert job is not None

# tests/unit/test_critic.py
class TestCriticAgent:
    def test_ruff_catches_syntax_errors(self, critic):
        """Test that ruff catches Python syntax errors"""
        code = "def foo(\n  invalid syntax"
        result = critic.validate(code)
        assert result.passed is False
        assert "syntax" in result.errors[0].lower()
    
    def test_bandit_catches_security_issues(self, critic):
        """Test that bandit catches security issues"""
        code = """
import subprocess
subprocess.call(user_input, shell=True)  # Security issue
"""
        result = critic.validate(code)
        assert result.passed is False
        assert any("security" in e.lower() or "subprocess" in e.lower() for e in result.errors)
    
    def test_valid_code_passes(self, critic):
        """Test that valid Python code passes"""
        code = """
def calculate_sum(a, b):
    return a + b

result = calculate_sum(1, 2)
print(result)
"""
        result = critic.validate(code)
        assert result.passed is True

# tests/unit/test_sandbox.py
class TestSandbox:
    def test_resource_limits_enforced(self, sandbox):
        """Test that resource limits are enforced"""
        result = sandbox.execute(
            code="while True: pass",  # Infinite loop
            timeout=5
        )
        assert result.status == "timeout"
        assert result.execution_time >= 5
    
    def test_network_access_denied(self, sandbox):
        """Test that network access is blocked"""
        code = """
import urllib.request
response = urllib.request.urlopen('http://google.com')
"""
        result = sandbox.execute(code)
        assert result.status == "error"
        assert "network" in result.error.lower() or "connection" in result.error.lower()
    
    def test_filesystem_readonly(self, sandbox):
        """Test that system files are read-only"""
        code = """
with open('/etc/passwd', 'w') as f:
    f.write('hacked')
"""
        result = sandbox.execute(code)
        assert result.status == "error"
        assert "permission" in result.error.lower()
    
    def test_python_only(self, sandbox):
        """Test that only Python code is executed"""
        # Sandbox should only accept Python
        result = sandbox.execute("console.log('hello')", language="javascript")
        assert result.status == "error"
        assert "unsupported" in result.error.lower() or "python only" in result.error.lower()
```

### Frontend Unit Tests

```typescript
// tests/unit/useJobs.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useJobs } from '@/hooks/useJobs';

describe('useJobs', () => {
  it('fetches jobs on mount', async () => {
    const { result } = renderHook(() => useJobs());
    
    await waitFor(() => {
      expect(result.current.jobs).toHaveLength(2);
      expect(result.current.loading).toBe(false);
    });
  });
  
  it('handles fetch errors gracefully', async () => {
    global.fetch = jest.fn(() => 
      Promise.reject(new Error('Network error'))
    );
    
    const { result } = renderHook(() => useJobs());
    
    await waitFor(() => {
      expect(result.current.error).toBe('Failed to fetch jobs');
      expect(result.current.jobs).toHaveLength(0);
    });
  });
});

// tests/unit/ImageUpload.test.tsx
describe('ImageUpload', () => {
  it('accepts only image files', () => {
    const { getByTestId } = render(<ImageUpload />);
    const input = getByTestId('file-input');
    
    // Should accept PNG
    fireEvent.change(input, { target: { files: [new File([''], 'test.png', { type: 'image/png' })] } });
    expect(screen.queryByText('Invalid file type')).not.toBeInTheDocument();
  });
  
  it('rejects non-image files', () => {
    const { getByTestId } = render(<ImageUpload />);
    const input = getByTestId('file-input');
    
    // Should reject PDF
    fireEvent.change(input, { target: { files: [new File([''], 'test.pdf', { type: 'application/pdf' })] } });
    expect(screen.getByText('Invalid file type')).toBeInTheDocument();
  });
});
```

---

## 🔗 Integration Tests

### API Integration Tests

```python
# tests/integration/test_api_flow.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestAPIFlow:
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self):
        return {"Authorization": "Bearer test_token"}
    
    def test_full_job_flow(self, client, auth_headers):
        """Test complete job flow from upload to results"""
        
        # 1. Upload image (PNG only)
        with open("tests/fixtures/images/test_chart.png", "rb") as f:
            response = client.post(
                "/api/v1/files/upload",
                files={"file": ("test.png", f, "image/png")},
                headers=auth_headers
            )
        assert response.status_code == 200
        file_id = response.json()["file_id"]
        
        # 2. Create job
        response = client.post(
            "/api/v1/jobs",
            json={"file_id": file_id, "task": "analyze"},
            headers=auth_headers
        )
        assert response.status_code == 201
        job_id = response.json()["job_id"]
        
        # 3. Wait for completion (with timeout)
        import time
        for _ in range(30):
            response = client.get(f"/api/v1/jobs/{job_id}", headers=auth_headers)
            if response.json()["status"] in ["completed", "failed"]:
                break
            time.sleep(1)
        
        # 4. Verify results
        assert response.json()["status"] == "completed"
        assert "result" in response.json()
    
    def test_reject_pdf_upload(self, client, auth_headers):
        """Test that PDF uploads are rejected"""
        with open("tests/fixtures/test.pdf", "rb") as f:
            response = client.post(
                "/api/v1/files/upload",
                files={"file": ("test.pdf", f, "application/pdf")},
                headers=auth_headers
            )
        assert response.status_code == 400
        assert "image" in response.json()["detail"].lower()

# tests/integration/test_critic_integration.py
class TestCriticIntegration:
    def test_critic_blocks_dangerous_code(self, agent_pipeline):
        """Test that critic blocks dangerous code before sandbox"""
        dangerous_code = """
import os
os.system("rm -rf /")
"""
        result = agent_pipeline.process_code(dangerous_code)
        assert result.validation_passed is False
        assert result.sandbox_executed is False  # Should never reach sandbox
    
    def test_critic_allows_safe_code(self, agent_pipeline):
        """Test that critic allows safe code through"""
        safe_code = """
import matplotlib.pyplot as plt
plt.bar(['A', 'B'], [1, 2])
plt.savefig('/tmp/output.png')
"""
        result = agent_pipeline.process_code(safe_code)
        assert result.validation_passed is True
        assert result.sandbox_executed is True
```

---

## 🚀 End-to-End Tests

### Core E2E Scenarios

```python
# tests/e2e/test_core_flows.py
import pytest
from playwright.sync_api import Page, expect

class TestE2EFlows:
    @pytest.fixture
    def authenticated_page(self, page: Page):
        """Login and return authenticated page"""
        page.goto("http://localhost:3000")
        page.click("text=Sign In")
        page.fill("input[name=email]", "test@example.com")
        page.fill("input[name=password]", "password123")
        page.click("button[type=submit]")
        expect(page).to_have_url("http://localhost:3000/dashboard")
        return page
    
    def test_image_analysis_flow(self, authenticated_page: Page):
        """Test complete image analysis flow"""
        page = authenticated_page
        
        # Upload image (PNG only)
        page.click("text=New Analysis")
        page.set_input_files("input[type=file]", "tests/fixtures/images/chart.png")
        page.click("text=Upload")
        
        # Wait for processing
        expect(page.locator("text=Processing")).to_be_visible()
        expect(page.locator("text=Completed")).to_be_visible(timeout=60000)
        
        # Verify results (static chart)
        expect(page.locator(".result-container")).to_contain_text("Analysis")
        expect(page.locator("img.generated-chart")).to_be_visible()
    
    def test_code_validation_shown(self, authenticated_page: Page):
        """Test that code validation status is shown"""
        page = authenticated_page
        
        page.click("text=New Analysis")
        page.set_input_files("input[type=file]", "tests/fixtures/images/chart.png")
        page.click("text=Upload")
        
        # Verify validation step is shown
        expect(page.locator("text=Validating code")).to_be_visible(timeout=30000)
        expect(page.locator("text=Validation passed")).to_be_visible(timeout=10000)

# tests/e2e/test_error_recovery.py
class TestErrorRecovery:
    def test_validation_failure_shown_to_user(self, authenticated_page: Page):
        """Test that validation failures are shown to user"""
        # This would require mocking the agent to generate bad code
        # User should see clear error message with options
        pass
    
    def test_sandbox_timeout_notification(self, authenticated_page: Page):
        """Test that sandbox timeout shows proper notification"""
        # User should see timeout error with retry option
        pass
```

---

## 🛡️ Security Tests

```python
# tests/security/test_sandbox_escape.py
class TestSandboxSecurity:
    def test_cannot_access_host_files(self, sandbox):
        """Verify sandbox cannot read host files"""
        codes = [
            "open('/etc/shadow', 'r').read()",
            "import os; os.system('cat /etc/passwd')",
            "__import__('subprocess').run(['ls', '/'])",
        ]
        
        for code in codes:
            result = sandbox.execute(code)
            assert result.status == "error"
    
    def test_cannot_make_network_requests(self, sandbox):
        """Verify network isolation"""
        codes = [
            "import urllib.request; urllib.request.urlopen('http://evil.com')",
            "import socket; socket.socket().connect(('8.8.8.8', 53))",
        ]
        
        for code in codes:
            result = sandbox.execute(code)
            assert result.status == "error"
    
    def test_resource_bomb_prevention(self, sandbox):
        """Test protection against resource exhaustion"""
        codes = [
            "a = [0] * (10**10)",  # Memory bomb
            "[i for i in range(10**20)]",  # CPU bomb
        ]
        
        for code in codes:
            result = sandbox.execute(code, timeout=5)
            assert result.status in ["error", "timeout"]

# tests/security/test_input_validation.py
class TestInputValidation:
    def test_only_images_accepted(self, client, auth_headers):
        """Test that only image files are accepted"""
        invalid_files = [
            ("test.pdf", "application/pdf"),
            ("test.exe", "application/x-executable"),
            ("test.js", "application/javascript"),
            ("test.py", "text/x-python"),
        ]
        
        for filename, mimetype in invalid_files:
            response = client.post(
                "/api/v1/files/upload",
                files={"file": (filename, b"content", mimetype)},
                headers=auth_headers
            )
            assert response.status_code == 400
```

---

## 🚨 Error Handling Strategy

### Error Classification

```python
# app/core/exceptions.py
from enum import Enum

class ErrorSeverity(Enum):
    LOW = "low"        # Log and continue
    MEDIUM = "medium"  # Notify user, offer retry
    HIGH = "high"      # Fail job, notify user
    CRITICAL = "critical"  # Stop system, alert admin

class ErrorCategory(Enum):
    USER_INPUT = "user_input"
    MODEL_ERROR = "model_error"
    VALIDATION_ERROR = "validation_error"  # Critic agent failures
    SANDBOX_ERROR = "sandbox_error"
    SYSTEM_ERROR = "system_error"

class ApplicationError(Exception):
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity,
        category: ErrorCategory,
        user_message: str = None,
        remediation: list = None
    ):
        self.message = message
        self.severity = severity
        self.category = category
        self.user_message = user_message or message
        self.remediation = remediation or []
```

### Critic Agent Error Handling

```python
# app/services/error_recovery.py
class ErrorRecoveryService:
    def handle_validation_error(self, error: Exception, context: dict):
        """Handle code validation failures"""
        
        if "ruff" in str(error).lower():
            return ApplicationError(
                message=f"Linting error: {error}",
                severity=ErrorSeverity.MEDIUM,
                category=ErrorCategory.VALIDATION_ERROR,
                user_message="Generated code has syntax issues",
                remediation=[
                    "View the generated code",
                    "Request regeneration with different prompt",
                    "Download code and fix manually"
                ]
            )
        
        elif "bandit" in str(error).lower() or "security" in str(error).lower():
            return ApplicationError(
                message=f"Security issue: {error}",
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.VALIDATION_ERROR,
                user_message="Generated code has potential security issues",
                remediation=[
                    "View security report",
                    "Request safer implementation",
                    "Contact administrator for review"
                ]
            )
```

---

## ✅ Testing Checklist

### Before Each Commit
- [ ] Unit tests pass locally
- [ ] No linting errors
- [ ] Coverage maintained or improved

### Before Each PR
- [ ] All tests pass in CI
- [ ] Integration tests cover changes
- [ ] Security tests pass
- [ ] Critic agent tests pass
- [ ] Error scenarios tested

### Before Each Release
- [ ] Full E2E test suite passes
- [ ] Image upload/processing works
- [ ] Code validation (critic) works
- [ ] Sandbox isolation verified
- [ ] Rollback procedure tested

---

## 📝 Why This Testing Strategy

### Why Test Critic Agent Specifically?
The critic agent is a new component that validates code before sandbox execution. Testing it ensures we catch bugs and security issues before they reach the sandbox.

### Why Image-Only Upload Tests?
MVP only supports PNG/JPG. Tests verify we properly reject PDFs and other file types with clear error messages.

### Why Python-Only Sandbox Tests?
MVP only executes Python. Tests verify we reject non-Python code and properly handle Python-specific edge cases.

### Philosophy
> Test what matters for MVP. Every test serves the core image→analysis→code→validation→sandbox flow.