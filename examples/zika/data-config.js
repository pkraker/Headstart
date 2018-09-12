var data_config = {
    tag: "visualization",
    mode: "local_files",

    title: "Overview of the Zika Corpus",
    input_format: "json",
    base_unit: "readers",
    use_area_uri: true,
    is_force_areas: true,
	area_force_alpha: 0.015,
    url_prefix: "http://mendeley.com/catalog/",
    
    show_timeline: false,
    show_dropdown: false,
    show_intro: false,
    show_list: true,
    is_force_papers: true,
	content_based: true,
	sort_options: ["title", "authors", "year"],
	
	show_context: false,
	create_title_from_context: false,
	
	preview_type: "pdf",
	service: "pubmed",
	
	language: "eng_pubmed",
	doi_outlink: true,
    

    files: [{
        title: "edu1",
        file: "./data/output_zika.json"
    }]
};
