/**
 * Configuration for Industrial ML Course & Google Colab Integration
 * 
 * Edit the `githubUser` and `githubRepo` fields below to point to your GitHub
 * repository. This dynamically constructs the 1-click "Open in Google Colab" URLs
 * following the standard format:
 * https://colab.research.google.com/github/{user}/{repo}/blob/{branch}/public/notebooks/{file}
 */

export const CONFIG = {
  // Replace with your GitHub username or organization
  githubUser: 'max480425',

  // Replace with your repository name
  githubRepo: 'industrial-ml-course',

  // Target branch where notebooks are hosted
  githubBranch: 'main',

  // Base path inside repository pointing to notebook files
  notebooksPath: 'public/notebooks',

  // Colab URL generator
  getColabUrl: (notebookFileName) => {
    const { githubUser, githubRepo, githubBranch, notebooksPath } = CONFIG;
    const cleanFileName = notebookFileName.replace(/^\/+/, '');
    return `https://colab.research.google.com/github/${githubUser}/${githubRepo}/blob/${githubBranch}/${notebooksPath}/${cleanFileName}`;
  },

  // Direct local / static download URL for the notebook
  getNotebookDownloadUrl: (notebookFileName) => {
    const cleanFileName = notebookFileName.replace(/^\/+/, '');
    return `/notebooks/${cleanFileName}`;
  },

  // Project metadata
  siteTitle: 'Industrial Machine Learning & Predictive Maintenance',
  siteSubtitle: 'Dual-Language Interactive Engineering Lab (Simple EN & PL)',
  version: '1.0.0',
  totalModules: 7,
  totalLessons: 28,
};

export default CONFIG;
