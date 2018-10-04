var data_config = {
    tag: "visualization",
    mode: "local_files",
	
	service: "pubmed",

    title: "Overview of research articles in Wikidata",
    input_format: "json",
    base_unit: "readers",
    use_area_uri: true,
    is_force_areas: true,
	area_force_alpha: 0.015,
    
    show_timeline: false,
    show_dropdown: true,
    show_intro: false,
    show_list: true,
    is_force_papers: true,
	content_based: true,
	sort_options: ["title", "authors", "year"],
	
	show_context: false,
	create_title_from_context: false,
	
	preview_type: "pdf",
	
	language: "eng_pubmed",
	doi_outlink: true,
	
	filter_menu_dropdown: true,
    sort_menu_dropdown: true,
    filter_options: ["all", "open_access"],
	
	server_url: window.location.href.replace(/[^/]*$/, '') + "../../server/",
    

    files: [{
        title: "zika",
        file: "./data/output_zika.json"
    },
	{
        title: "invasive species",
        file: "./data/output_invasive_species.json"
    }]
};
