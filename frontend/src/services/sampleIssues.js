/**
 * Diverse pool of 8 realistic Kubernetes bug report samples.
 * Covers different SIG teams, completeness levels, and formats.
 */

export const SAMPLE_ISSUES = [
  {
    id: 1,
    tag: 'SIG Network (Incomplete - Missing Logs & Env)',
    shortLabel: 'SIG Network',
    badge: 'Incomplete Report',
    team: 'sig/network',
    repository: 'kubernetes/kubernetes',
    url: '',
    text: `Pod networking fails after restart\nAfter restarting a worker node, pods remain stuck in ContainerCreating and CNI plugin fails to initialize network namespaces.`,
  },
  {
    id: 2,
    tag: 'SIG Apps (Complete - Has Steps, Logs & Env)',
    shortLabel: 'SIG Apps',
    badge: 'Complete Report',
    team: 'sig/apps',
    repository: 'kubernetes/kubernetes',
    url: '',
    text: `Deployment rollout stuck in ProgressDeadlineExceeded on Kubernetes v1.29.2 (Ubuntu 22.04)\n\nSteps to reproduce:\n1. Apply Deployment with maxUnavailable: 0 and maxSurge: 1\n2. Trigger image update via kubectl set image\n3. Rollout hangs indefinitely\n\nError logs:\nE1014 replica_set.go:542] Sync "default/web-api" failed with ProgressDeadlineExceeded: ReplicaSet "web-api-7d9f8b" has timed out progressing.`,
  },
  {
    id: 3,
    tag: 'SIG Node (Missing Steps to Reproduce)',
    shortLabel: 'SIG Node',
    badge: 'Missing Steps',
    team: 'sig/node',
    repository: 'kubernetes/kubernetes',
    url: '',
    text: `Kubelet PLEG is not healthy and node status intermittently flips to NotReady\n\nEnvironment: Kubernetes v1.28.6, containerd v1.7.11, Linux kernel 6.1.\n\nRelevant logs:\nE1014 kubelet.go:1891] skipping pod synchronization - [PLEG is not healthy: pleg was last seen active 3m45s ago; threshold is 3m0s]`,
  },
  {
    id: 4,
    tag: 'SIG Storage (Complete - CSI Volume Attach Bug)',
    shortLabel: 'SIG Storage',
    badge: 'Complete CSI Bug',
    team: 'sig/storage',
    repository: 'kubernetes/kubernetes',
    url: '',
    text: `PersistentVolumeClaim stuck in Terminating and Multi-Attach error on AWS EBS CSI driver\n\nSteps to reproduce:\n1. Drain node with stateful pod attached to ReadWriteOnce PVC\n2. Pod reschedules to new node before VolumeAttachment detaches\n\nLogs:\nMulti-Attach error for volume "pvc-8f92a1" Volume is already exclusively attached to one node and can't be attached to another.\n\nEnvironment: EKS Kubernetes v1.29, aws-ebs-csi-driver v1.28.0`,
  },
  {
    id: 5,
    tag: 'SIG Scheduling (Missing Environment Details)',
    shortLabel: 'SIG Scheduling',
    badge: 'Missing Env',
    team: 'sig/scheduling',
    repository: 'kubernetes/kubernetes',
    url: '',
    text: `PodTopologySpreadConstraints ignored when combined with PodAntiAffinity during cluster scale-up\n\nSteps to reproduce:\n1. Deploy 12 replicas with maxSkew: 1 across 3 availability zones\n2. Add requiredDuringSchedulingIgnoredDuringExecution anti-affinity\n3. Scheduler places 6 pods in zone-a.\n\nLogs:\nI1014 schedule_one.go:214] Successfully bound pod to node-zone-a-3 despite topology skew violation.`,
  },
  {
    id: 6,
    tag: 'SIG API Machinery (Complete - Watch Cache Memory Leak)',
    shortLabel: 'SIG API Machinery',
    badge: 'Complete Memory Leak',
    team: 'sig/api-machinery',
    repository: 'kubernetes/kubernetes',
    url: '',
    text: `kube-apiserver memory usage spikes by 4GB during Informer relist with ResourceVersion=0\n\nSteps to reproduce:\n1. Start 50 custom controllers watching CustomResources with ResourceVersion="0"\n2. Trigger compaction on etcd\n\nLogs:\nW1014 watch_cache.go:418] watchChan buffer full (capacity 1000), dropping watch events for crd/v1alpha1\n\nEnvironment: Kubernetes v1.30.0, etcd 3.5.12, 64GB RAM control-plane`,
  },
  {
    id: 7,
    tag: 'SIG Auth (Missing Logs & Steps)',
    shortLabel: 'SIG Auth',
    badge: 'Missing Logs & Steps',
    team: 'sig/auth',
    repository: 'kubernetes/kubernetes',
    url: '',
    text: `BoundServiceAccountTokenVolume token rotation fails to refresh projected volume credentials before 1h expiry on Kubernetes v1.29`,
  },
  {
    id: 8,
    tag: 'GitHub URL Format Sample',
    shortLabel: 'GitHub Issue URL',
    badge: 'Live URL Format',
    team: 'sig/network',
    repository: 'kubernetes/kubernetes',
    url: 'https://github.com/kubernetes/kubernetes/issues/123456',
    text: `https://github.com/kubernetes/kubernetes/issues/123456: kube-proxy IPVS mode drops UDP packets when endpoint terminates gracefully on Kubernetes v1.28`,
  },
];

const LOCAL_STORAGE_KEY = 'bug_triage_sample_index';

/**
 * Gets the current sample index from localStorage or defaults to 0.
 */
export function getSavedSampleIndex() {
  try {
    const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (saved !== null) {
      const parsed = parseInt(saved, 10);
      if (!isNaN(parsed) && parsed >= 0 && parsed < SAMPLE_ISSUES.length) {
        return parsed;
      }
    }
  } catch {
    // ignore
  }
  return 0;
}

/**
 * Cycles to the next sample and saves the new index in localStorage.
 * Returns { sample, nextIndex }
 */
export function getNextSample(currentIndex = null) {
  const current = currentIndex !== null ? currentIndex : getSavedSampleIndex();
  const nextIndex = (current + 1) % SAMPLE_ISSUES.length;
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, nextIndex.toString());
  } catch {
    // ignore
  }
  return {
    sample: SAMPLE_ISSUES[nextIndex],
    nextIndex,
  };
}

/**
 * Returns a specific sample by index.
 */
export function getSampleByIndex(index) {
  const validIndex = ((index % SAMPLE_ISSUES.length) + SAMPLE_ISSUES.length) % SAMPLE_ISSUES.length;
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, validIndex.toString());
  } catch {
    // ignore
  }
  return {
    sample: SAMPLE_ISSUES[validIndex],
    index: validIndex,
  };
}
