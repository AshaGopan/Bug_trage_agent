/**
 * History persistence service using browser localStorage.
 * Pre-seeded with 3 realistic Kubernetes sample issues.
 */

const STORAGE_KEY = 'bug_triage_ai_history_v1';

export const INITIAL_SAMPLE_HISTORY = [
  {
    id: 'k8s-115201',
    title: 'iptables kube-proxy drops UDP fragments during pod network reloads',
    repository: 'kubernetes/kubernetes',
    url: 'https://github.com/kubernetes/kubernetes/issues/115201',
    suggestedTeam: 'SIG Network',
    predictedLabel: 'sig/network',
    confidence: 89.2,
    status: 'Triaged',
    dateAnalyzed: 'Oct 12, 2026',
    whyThisTeam: 'Identified high density of iptables chains, UDP packet drops, and kube-proxy packet filter rule resets. Strong cosine affinity with SIG Network historical issues.',
    similarIssues: [
      { issue_id: 108422, title: 'kube-proxy ipvs mode connection reset on heavy TCP traffic', label: 'sig/network', distance: 0.18 },
      { issue_id: 99341, title: 'CoreDNS resolution timeouts during calico CNI reload', label: 'sig/network', distance: 0.22 },
      { issue_id: 104523, title: 'NodePort service intermittent unreachable state', label: 'sig/network', distance: 0.29 },
    ],
    missingInfo: {
      stepsToReproduce: false,
      relevantLogs: false,
      environmentDetails: false,
    },
    suggestedResponse: `Thanks for opening this issue!

### SIG Assignment Recommendation
Based on our automated classification model (**89.2% confidence**), this report has been triaged for **\`sig/network\`** (SIG Network).

### 🔍 Potentially Related Issues
- #108422: kube-proxy ipvs mode connection reset on heavy TCP traffic
- #99341: CoreDNS resolution timeouts during calico CNI reload

*/sig network*`,
  },
  {
    id: 'k8s-124892',
    title: 'Kubelet memory regression: Cadvisor housekeeping fails to back off when memory.high is reached',
    repository: 'kubernetes/kubernetes',
    url: 'https://github.com/kubernetes/kubernetes/issues/124892',
    suggestedTeam: 'SIG Node',
    predictedLabel: 'sig/node',
    confidence: 86.5,
    status: 'Triaged',
    dateAnalyzed: 'Oct 13, 2026',
    whyThisTeam: 'Report concerns Kubelet daemon memory consumption, cgroups v2 memory.high controllers, and cadvisor container monitoring threads managed by SIG Node.',
    similarIssues: [
      { issue_id: 119402, title: 'Kubelet OOMKilled under high cgroup v2 memory pressure', label: 'sig/node', distance: 0.15 },
      { issue_id: 112399, title: 'Containerd CRI memory leak with rapid pod restarts', label: 'sig/node', distance: 0.21 },
      { issue_id: 108920, title: 'Kubelet eviction threshold delayed on cgroups v2', label: 'sig/node', distance: 0.27 },
    ],
    missingInfo: {
      stepsToReproduce: false,
      relevantLogs: false,
      environmentDetails: false,
    },
    suggestedResponse: `Thanks for opening this issue!

### SIG Assignment Recommendation
Based on our automated classification model (**86.5% confidence**), this report has been triaged for **\`sig/node\`** (SIG Node).

### 🔍 Potentially Related Issues
- #119402: Kubelet OOMKilled under high cgroup v2 memory pressure
- #112399: Containerd CRI memory leak with rapid pod restarts

*/sig node*`,
  },
  {
    id: 'k8s-118404',
    title: 'Intermittent CSI VolumeAttachment stuck in unmount loop during node drain',
    repository: 'kubernetes/kubernetes',
    url: 'https://github.com/kubernetes/kubernetes/issues/118404',
    suggestedTeam: 'SIG Storage',
    predictedLabel: 'sig/storage',
    confidence: 91.4,
    status: 'Triaged',
    dateAnalyzed: 'Oct 13, 2026',
    whyThisTeam: 'VolumeAttachment lifecycle controllers, attachdetach controller loops, and CSI driver storage unmount errors fall directly under SIG Storage.',
    similarIssues: [
      { issue_id: 106511, title: 'CSI nodeUnstageVolume timeout on NFS share', label: 'sig/storage', distance: 0.19 },
      { issue_id: 114220, title: 'PVC mount stuck in terminating phase', label: 'sig/storage', distance: 0.25 },
    ],
    missingInfo: {
      stepsToReproduce: false,
      relevantLogs: false,
      environmentDetails: false,
    },
    suggestedResponse: `Thanks for opening this issue!

### SIG Assignment Recommendation
Based on our automated classification model (**91.4% confidence**), this report has been triaged for **\`sig/storage\`** (SIG Storage).

*/sig storage*`,
  },
];

export function getHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_SAMPLE_HISTORY));
      return INITIAL_SAMPLE_HISTORY;
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : INITIAL_SAMPLE_HISTORY;
  } catch {
    return INITIAL_SAMPLE_HISTORY;
  }
}

export function saveHistory(records) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
  } catch (e) {
    console.error('Failed to save history to localStorage', e);
  }
}

export function addHistoryRecord(record) {
  const current = getHistory();
  const updated = [record, ...current.filter((item) => item.id !== record.id)].slice(0, 50);
  saveHistory(updated);
  return updated;
}
