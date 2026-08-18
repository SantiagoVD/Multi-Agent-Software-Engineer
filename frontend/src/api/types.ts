export type TaskStatus =
  | 'received'
  | 'cloning_repository'
  | 'analyzing_repository'
  | 'developing'
  | 'testing'
  | 'reviewing'
  | 'completed'
  | 'failed'

export interface TaskRequest {
  repository_url: string
  task: string
  branch?: string | null
  publish_branch?: boolean
}

export interface TestIssue {
  test_name?: string | null
  message: string
  file?: string | null
}

export interface TestResult {
  success: boolean
  available: boolean
  command: string
  passed: number
  failed: number
  skipped: number
  exit_code?: number | null
  timed_out: boolean
  issues: TestIssue[]
  raw_output?: string | null
}

export type IssueSeverity = 'low' | 'medium' | 'high' | 'critical'
export type ReviewStatus = 'approved' | 'changes_required'

export interface ReviewIssue {
  severity: IssueSeverity
  description: string
  file?: string | null
  line?: number | null
  recommendation?: string | null
}

export interface ReviewResult {
  status: ReviewStatus
  summary: string
  issues: ReviewIssue[]
}

export interface FinalResult {
  task_id: string
  status: TaskStatus
  success: boolean
  summary: string
  files_modified: string[]
  test_result?: TestResult | null
  review_result?: ReviewResult | null
  publication?: BranchPublication | null
  iterations: number
}

export interface BranchPublication {
  requested: boolean
  published: boolean
  branch?: string | null
  remote: string
  commit?: string | null
  message: string
}

export interface HealthResult { status: string }

export interface OllamaHealthResult {
  status: 'online' | 'offline'
  model: string
  model_available: boolean
}
