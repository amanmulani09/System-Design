from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Dict
from datetime import datetime
import uuid


# =========================
# ENUMS
# =========================

class IssueStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# =========================
# ENTITIES
# =========================

class Customer:
    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email


class Agent:
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.active_issues: List[str] = []


class Issue:
    def __init__(self, title: str, description: str,
                 customer: Customer, priority: Priority):
        self.issue_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.customer = customer
        self.priority = priority
        self.status = IssueStatus.OPEN
        self.agent: Optional[Agent] = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.history: List[str] = []

    def assign_agent(self, agent: Agent):
        self.agent = agent
        self.status = IssueStatus.IN_PROGRESS
        agent.active_issues.append(self.issue_id)
        self._add_history(f"Issue assigned to agent {agent.name}")

    def resolve(self):
        if self.status != IssueStatus.IN_PROGRESS:
            raise Exception("Issue must be IN_PROGRESS to resolve.")
        self.status = IssueStatus.RESOLVED
        self.updated_at = datetime.now()
        self._add_history("Issue resolved")

    def close(self):
        if self.status != IssueStatus.RESOLVED:
            raise Exception("Issue must be RESOLVED to close.")
        self.status = IssueStatus.CLOSED
        self.updated_at = datetime.now()
        self._add_history("Issue closed")

    def _add_history(self, action: str):
        timestamp = datetime.now().isoformat()
        self.history.append(f"{timestamp} - {action}")


# =========================
# REPOSITORY (Interface)
# =========================

class IssueRepository(ABC):

    @abstractmethod
    def save(self, issue: Issue):
        pass

    @abstractmethod
    def get_by_id(self, issue_id: str) -> Optional[Issue]:
        pass

    @abstractmethod
    def get_all(self) -> List[Issue]:
        pass


# =========================
# IN-MEMORY REPOSITORY
# =========================

class InMemoryIssueRepository(IssueRepository):

    def __init__(self):
        self.issues: Dict[str, Issue] = {}

    def save(self, issue: Issue):
        self.issues[issue.issue_id] = issue

    def get_by_id(self, issue_id: str) -> Optional[Issue]:
        return self.issues.get(issue_id)

    def get_all(self) -> List[Issue]:
        return list(self.issues.values())


# =========================
# SERVICE LAYER
# =========================

class IssueService:

    def __init__(self, repository: IssueRepository):
        self.repository = repository

    def create_issue(self, title: str, description: str,
                     customer: Customer, priority: Priority) -> Issue:
        issue = Issue(title, description, customer, priority)
        self.repository.save(issue)
        return issue

    def assign_issue(self, issue_id: str, agent: Agent):
        issue = self._get_issue_or_raise(issue_id)
        issue.assign_agent(agent)
        self.repository.save(issue)

    def resolve_issue(self, issue_id: str):
        issue = self._get_issue_or_raise(issue_id)
        issue.resolve()
        self.repository.save(issue)

    def close_issue(self, issue_id: str):
        issue = self._get_issue_or_raise(issue_id)
        issue.close()
        self.repository.save(issue)

    def get_issues_by_status(self, status: IssueStatus) -> List[Issue]:
        return [
            issue for issue in self.repository.get_all()
            if issue.status == status
        ]

    def get_issues_by_agent(self, agent_id: str) -> List[Issue]:
        return [
            issue for issue in self.repository.get_all()
            if issue.agent and issue.agent.agent_id == agent_id
        ]

    def _get_issue_or_raise(self, issue_id: str) -> Issue:
        issue = self.repository.get_by_id(issue_id)
        if not issue:
            raise Exception("Issue not found")
        return issue


# =========================
# MAIN (Usage Example)
# =========================

if __name__ == "__main__":

    repository = InMemoryIssueRepository()
    service = IssueService(repository)

    # Create customer & agent
    customer = Customer("C1", "John Doe", "john@example.com")
    agent = Agent("A1", "Agent Smith")

    # Create issue
    issue = service.create_issue(
        "Payment Failure",
        "Payment not going through",
        customer,
        Priority.HIGH
    )

    print(f"Issue Created: {issue.issue_id}")

    # Assign issue
    service.assign_issue(issue.issue_id, agent)

    # Resolve issue
    service.resolve_issue(issue.issue_id)

    # Close issue
    service.close_issue(issue.issue_id)

    print("Issue Status:", issue.status)
    print("History:", issue.history)
