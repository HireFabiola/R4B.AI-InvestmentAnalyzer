from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PropertyInfo:
    address: str
    asking_price: float
    listing_url: Optional[str] = None
    description: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[int] = None
    year_built: Optional[int] = None
    photos: list[str] = field(default_factory=list)


@dataclass
class ScreeningResult:
    next_action: Optional[str] = None
    recommendation: Optional[str] = None
    reasoning: Optional[str] = None
    flags: list[str] = field(default_factory=list)
    key_flags: list[str] = field(default_factory=list)
    positive_signals: list[str] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    opportunity_score: Optional[int] = None
    screening_score: Optional[int] = None
    information_completeness: Optional[float] = None
    metrics: dict[str, float] = field(default_factory=dict)


@dataclass
class MarketAnalysis:
    estimated_arv: Optional[float] = None
    comparable_sales: list[dict] = field(default_factory=list)
    market_summary: Optional[str] = None
    market_risks: list[str] = field(default_factory=list)


@dataclass
class RehabAnalysis:
    condition_summary: Optional[str] = None
    estimated_repair_cost: Optional[float] = None
    repair_risks: list[str] = field(default_factory=list)
    major_concerns: list[str] = field(default_factory=list)


@dataclass
class FinancialAnalysis:
    purchase_price: Optional[float] = None
    repair_cost: Optional[float] = None
    holding_costs: Optional[float] = None
    selling_costs: Optional[float] = None
    total_project_cost: Optional[float] = None
    potential_profit: Optional[float] = None
    estimated_roi: Optional[float] = None


@dataclass
class StrategyRecommendation:
    recommended_strategy: Optional[str] = None
    recommendation: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    remaining_risks: list[str] = field(default_factory=list)


@dataclass
class PropertyState:
    property_info: PropertyInfo
    screening: ScreeningResult = field(default_factory=ScreeningResult)
    market: MarketAnalysis = field(default_factory=MarketAnalysis)
    rehab: RehabAnalysis = field(default_factory=RehabAnalysis)
    financials: FinancialAnalysis = field(default_factory=FinancialAnalysis)
    strategy: StrategyRecommendation = field(default_factory=StrategyRecommendation)

    current_stage: str = "created"
    workflow_status: str = "in_progress"
