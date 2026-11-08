export type ExecutionMode = 'code_sandbox' | 'browser_sandbox' | 'redteam_probe';

export type TaskStatus =
  | 'VERIFIED_EXECUTION'
  | 'CONTAINED_THREAT'
  | 'SELF_HEALED_SUCCESS'
  | 'EXECUTION_ERROR';

export interface PipelineStage {
  id: string;
  stepNumber: number;
  title: string;
  modelOrRuntime: string;
  status: 'pending' | 'running' | 'passed' | 'blocked' | 'healed' | 'failed';
  durationMs: number;
  detail: string;
}

export interface DeterministicCheck {
  name: string;
  passed: boolean;
  detail: string;
}

export interface SecurityEvent {
  timestamp: string;
  layer: 'NEMOTRON_PREFLIGHT' | 'AST_POLICY_SCAN' | 'DOCKER_CGROUP' | 'NETNS_FIREWALL' | 'SECCOMP_BPF';
  severity: 'INFO' | 'WARN' | 'BLOCKED';
  vector: string;
  actionTaken: string;
  ruleId: string;
}

export interface ArtifactItem {
  name: string;
  type: 'svg_chart' | 'playwright_screenshot' | 'csv_summary' | 'python_script' | 'dom_report';
  sha256: string;
  sizeBytes: number;
  previewData?: string;
  metadata?: Record<string, string | number>;
}

export interface ProofReceipt {
  receiptId: string;
  taskTitle: string;
  prompt: string;
  mode: ExecutionMode;
  targetUrl?: string;
  status: TaskStatus;
  createdAt: string;
  totalDurationMs: number;
  vultrInfra: {
    vmHostname: string;
    vmRegion: string;
    inferenceEndpoint: string;
    safetyModel: string;
    plannerModel: string;
    verifierModel: string;
  };
  containerLifecycle: {
    containerId: string;
    image: string;
    isolationFlags: string[];
    networkPolicy: string;
    secretsInjected: number;
    spawnedAt: string;
    destroyedAt: string;
    cleanupVerified: boolean;
    exitCode: number;
  };
  resourceUsage: {
    cpuLimitCores: number;
    cpuPeakPercent: number;
    memoryLimitMb: number;
    memoryPeakMb: number;
    pidsLimit: number;
    pidsPeak: number;
    timeoutSec: number;
    networkEgressBytes: number;
  };
  pipelineStages: PipelineStage[];
  generatedCode: string;
  selfHealingLog?: {
    attempt1Code?: string;
    attempt1Error: string;
    patchApplied: string;
    unifiedDiff?: string;
    repairModel?: string;
  };
  stdout: string;
  stderr: string;
  verifierSummary: string;
  deterministicChecks?: DeterministicCheck[];
  securityEvents: SecurityEvent[];
  artifacts: ArtifactItem[];
  cryptographicProof: {
    inputSha256: string;
    codeSha256: string;
    stdoutSha256: string;
    receiptSignatureSha256: string;
    ed25519PublicKeyHex?: string;
    ed25519PublicKeyPem?: string;
    canonicalPayloadJson?: string;
    verificationAlgorithm: string;
  };
}

export interface PresetScenario {
  id: string;
  title: string;
  badge: string;
  mode: ExecutionMode;
  prompt: string;
  targetUrl?: string;
  sampleCsvName?: string;
  expectedOutcome: string;
  mockReceiptId: string;
}
