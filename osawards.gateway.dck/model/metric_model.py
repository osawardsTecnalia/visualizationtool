from enum import Enum


class Metric(str, Enum):
    #Activity Indicators
    act_repos = ("Activity Indicators: Number of GitHub repositories", "act_repos_year_country.csv")
    act_contributors = ("Activity Indicators: Number of GitHub contributors", "act_contributors_year_country.csv")
    act_commits = ("Activity Indicators: Number of GitHub commits", "act_commits_year_country.csv")
    act_stars = ("Activity Indicators: Number of GitHub stars", "act_stars_year_country.csv")
    act_watches = ("Activity Indicators: Number of GitHub watches", "act_watches_year_country.csv")
    act_forks = ("Activity Indicators: Number of GitHub forks", "act_forks_year_country.csv")
    
    # Ecosystem Indicators
    eco_commit_intensity = ("Ecosystem Indicators: GitHub Commit Intensity", "eco_commit_intensity_year_country.csv")
    eco_contributor_density = ("Ecosystem Indicators: GitHub Contributor Intensity", "eco_contributor_density_year_country.csv")
    eco_popularity_index = ("Ecosystem Indicators: GitHub Popularity Index", "eco_popularity_year_country.csv")
    eco_repo_ownership_intensity = ("Ecosystem Indicators: GitHub Repository Ownership Intensity", "eco_repository_ownership_year_country.csv")
    eco_retention_rate = ("Ecosystem Indicators: GitHub Retention Rate", "eco_retention_year_country.csv")
    eco_turnover_rate = ("Ecosystem Indicators: GitHub Turnover Rate", "eco_turnover_year_country.csv")
    
    # Other Dashboards
    #oth_patents = ("Other Dashboards: Total Patents (PATSTAT)", "oth_patents_total_year_country.csv")
    oth_publications = ("Other Dashboards: Total Publications (SCOPUS)", "oth_publications_total_year_country.csv")
    oth_osh = ("Other Dashboards: Certified Open-Source Hardware Projects", "oth_osh_projects.csv")
    oth_cern = ("Other Dashboards: CERN Open-Hardware Repository", "oth_cern_projects.csv")
    oth_ec_osor_solutions = ("Other Dashboards: EC Open-Source Observatory Solutions", "oth_ec_osor_solutions.csv")
    
    # Blog Posts
    bp1_share_repo_creation = ("Blog Posts: BP1: Share of EU Repository Creation by Country", "bp1_share_repo_creation_year_country.csv")
    bp1_share_os_companies = ("Blog Posts: BP1: Share of OS Companies by Country in all EU-27 OS Companies", "bp1_share_os_companies_in_all_eu27_os_companies.csv")
    bp1_cumulative_os_repos = ("Blog Posts: BP1: Cumulative Open-Source Repositories", "bp1_cumulative_os_repos_year_country.csv")
    bp1_cumulative_share_os_repos = ("Blog Posts: BP1: Cumulative Share of Global Open-Source Repositories", "bp1_cumulative_share_global_os_repos_year_country.csv")
    bp2_professionalization_eu27_us_cn = ("Blog Posts: BP2: Professionalization: EU-27 vs United States vs China", "bp2_professionalization_eu27_us_cn.csv")
    bp2_professionalization_repos_organization = ("Blog Posts: BP2: Professionalization: Repositories per Organization", "bp2_professionalization_global_benchmark.csv")
    bp2_professionalization_commit_share = ("Blog Posts: BP2: Professionalization: Share of GitHub Commits by EU-27 Countries in 2023", "bp2_professionalization_eu27_commit_share.csv")
    bp2_professionalization_population = ("Blog Posts: BP2: Professionalization: EU-27 Normalized by Population Size", "bp2_professionalization_population_normalized.csv")
    bp3_maintenance_commit_intensity = ("Blog Posts: BP3: Maintenance: Commit intensity: The EU-27 in an international comparison", "bp3_maintenance_commit_intensity.csv")
    bp3_maintenance_retention = ("Blog Posts: BP3: Maintenance: Retention rate, EU-27 vs United States vs China", "bp3_maintenance_retention.csv")
    bp3_maintenance_turnover = ("Blog Posts: BP3: Maintenance: Turnover rate, EU-27 vs United States vs China", "bp3_maintenance_turnover.csv")
    bp3_maintenance_commit_intensity_eu27 = ("Blog Posts: BP3: Maintenance: Commit intensity across the EU-27 countries in 2023", "bp3_maintenance_eu27_commit_intensity.csv")
    bp3_maintenance_retention_eu27 = ("Blog Posts: BP3: Maintenance: Retention rate across the EU-27 countries in 2023", "bp3_maintenance_eu27_retention.csv")
    bp3_maintenance_turnover_eu27 = ("Blog Posts: BP3: Maintenance: Turnover rate across the EU-27 countries in 2023", "bp3_maintenance_eu27_turnover.csv")
    
    def __new__(cls, label, filename):
        obj = str.__new__(cls, label)
        obj._value_ = label
        obj.filename = filename
        return obj
