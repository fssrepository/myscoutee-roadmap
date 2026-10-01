import json,pathlib
O=pathlib.Path(__file__).resolve().parent
spec={
'e-kozig':[
(16,'feat: establish the Angular administration portal and document module','Create the Angular and Material application, lazy document module, initial document UI and GitHub Pages output. Keep the setup fixes and generated deployment files with their source snapshot.'),
(30,'feat: add portal sections and document search filters','Add home, appointments, information and office sections. Complete document search, date ranges, columns and accordion behavior, together with Pages configuration and rebuilt assets.'),
(40,'fix: refine document filtering and responsive layouts','Consolidate mobile and desktop layout fixes, search widths, loading indicators and document filtering with the corresponding generated site.'),
(61,'docs: introduce e-kozig branding and process overview','Rename the project to e-kozig, add the process illustration and feature plans, and consolidate the README naming and link revisions.'),
(75,'feat: refine the home page and feature overview','Update home-page content, captions, layout and routes alongside feature plans and documentation. Preserve the final result of the intermediate cleanup and revert.'),
(86,'fix: complete document statuses drafts and detail popups','Refine document rendering, draft handling, pending-acceptance state, action buttons and detail-popup styles, including the accompanying home-page adjustments.'),
(96,'feat: implement invoice lists and period filtering','Add the invoice screen and refine period ordering, table styles, filter popups and filter controls with the generated Pages assets.'),
(106,'fix: refine case search and portal navigation','Improve case-number search, home-page wording, navigation menus and badges; retain the related planning cleanup and rebuilt site.'),
(127,'feat: refine account selection and portal dialogs','Develop account-selector navigation, Material-style alerts, case loading, scrolling and avatars. Include the related feature-plan, wording, invoice-navigation and button fixes.'),
(139,'fix: improve responsive alignment and mobile popups','Consolidate portal and document alignment, home-page styling, full-screen mobile popups and button fixes with their deployment output.'),
(146,'fix: align document layouts and development build defaults','Refine application and document/invoice layout styles and set the development build defaults in the Angular and package configuration.'),
(154,'feat: explain the administration and tax-system model','Update the home-page explanation, navigation and README, introduce the tax-system illustration, and consolidate the associated styling and Pages rebuilds.'),
(194,'feat: add the visual form editor','Introduce the admin form editor, its models and store, canvas controls, filtering and multi-selection. Consolidate editor cleanup and fixes, the intervening document-load adjustment, and the published site snapshot.'),
(196,'fix: finalize form-editor behavior and portal presentation','Preserve the final editor and documentation corrections, routing and presentation updates, generated site output, and application TypeScript configuration.')],
'myscoutee-old':[
(5,'feat: import the archived MyScoutee frontend prototype','Import the clean Angular frontend snapshot, configure GitHub Pages, normalize environment and index settings, and add project links.'),
(9,'fix: complete demo data and development cache handling','Add sample data and transformation/list refinements, update generated assets, and consolidate development-cache, watch synchronization and service-worker hash fixes.'),
(12,'chore: archive campaign drafts and promotional videos','Preserve the campaign form backup, promotional video files and archived task notes as one historical snapshot.'),
(13,'docs: update the UI prototype link','Point the README UI prototype link to its corrected destination.')],
'millennium-math-problems':[
(16,'research: establish the Navier-Stokes numerical experiment suite','Introduce the C++ spectral and lemma tooling, gradient and L-BFGS searches, critical-integral experiments, local/nonlocal partitions and far-tail investigations. Retain their numerical outputs, certificates and failed-lemma records as historical research evidence.'),
(26,'research: investigate helical sectors and local triad geometry','Develop dyadic and far-tail ledgers, transition blocks, helicity-sector searches and cutoff scans, with local symmetry and orthogonal-triad experiments and supporting reports.'),
(37,'research: develop local-signature and coupled-integral searches','Introduce local-signature families, gradient and trajectory experiments, coupled-integral and factor searches, and supporting numerical and adjoint updates. Preserve their recorded outcomes and limitations.'),
(50,'research: explore shifted local density and cyclic closure models','Develop shifted-density budgets, quartic identities, commutator and projected-residual ledgers, closure targets and signature blocks. Extend cyclic, trajectory, Krylov and response-family experiments with their recorded evidence.'),
(58,'research: organize response tensors and remainder-quartet experiments','Reorganize research sources and add response-diagonal/tensor investigations, doubling-scale ledgers, remainder absorption and tradeoff experiments, and equal-low geometry analysis.'),
(64,'research: explore projective quartet and cross-power structure','Introduce projective geometry, coherence and fan scans, stretching and cross-power objectives, diagonal kernels and attribution ledgers with the associated experiment records.'),
(77,'research: investigate projective height and commutator bounds','Develop finite projective families, core/tail scans, height-transfer matrices and Schur summaries, envelope and commutator-ratio searches, and coercivity-path and dynamic-ratio experiments.'),
(82,'refactor: organize local-density research modules','Consolidate the research source reorganization across analysis, core, objective and optimization modules, retaining the accompanying experiment records and documentation.'),
(96,'research: explore projective normalization and tail tradeoffs','Develop normalization objectives, matrix and tail summaries, scans, core/tail alignment and alternating searches, including the recorded normalization-tail and projective-height investigations.'),
(101,'research: extend normalization alignment and tail diagnostics','Add alignment and Cauchy objectives, longer continuation runs, gap attribution and correlation diagnostics, satellite scans and tail-Schur tooling with their numerical evidence. These are historical research snapshots, not a claim of a continuous Navier-Stokes proof.'),
(112,'docs: publish the project overview and Navier-Stokes briefs','Add and refine the repository overview, presentation generators, illustrations, PDF/PPTX project pitch and plain-language research briefs.'),
(123,'docs: develop the Navier-Stokes video production package','Build the storyboard, narration, captions and production workflow; consolidate English localization, platform-cost guidance, AI-research context, prompts and initial production assets.'),
(129,'chore: organize video production assets and handoff','Preserve preview renders, restructure story/production/platform/editorial materials, and consolidate storyboard, edit-plan and production-handoff revisions.'),
(135,'media: finalize the research video and publication materials','Consolidate final video renders and overlays, quality-control and editing scripts, publication copy and cover artwork, mobile-header corrections and the README update.'),
(137,'fix: withdraw amplitude-inhomogeneous normalization claims','Preserve the explicit withdrawal and correction of PNT claims across the research plans, evidence ledger and handoff, together with the final PNT-12 README clarification.')]
}
plan={}
for name,groups in spec.items():
 inv=json.loads((O/(name+'-inventory.json')).read_text())
 plan[name]=[[inv[end-1]['sha'],title,body] for end,title,body in groups]
 assert groups[-1][0]==len(inv)
(O/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
for n,v in plan.items():print(n,len(v),'groups')
