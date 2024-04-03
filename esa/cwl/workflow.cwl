$graph:

- class: Workflow
  doc: Get and merge DEM over a BBOx area
  id: get-dem-theo
  inputs:
    s_bbox:
      doc: Bounding box
      label:  Bounding box
      type: string
    s_compute:
      doc: TRUE to enable heavy computation 
      label: Compute
      type: string
  label: s expressions
  outputs:
  - id: wf_outputs
    outputSource:
    - /projects/data/output
    type:
      Directory[]

- baseCommand: /opt/entrypoint.sh
  class: CommandLineTool

  id: driver-command

  arguments:
  - --bbox
  - valueFrom: $( inputs.s_bbox )
  - --compute
  - valueFrom: $( inputs.s_compute )

  requirements:
    DockerRequirement:
      dockerPull: registry.eu-west-0.prod-cloud-ocb.orange-business.com/esa-maap.org/esa-maap-dev/get-dem:latest

cwlVersion: v1.0

$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.3.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf
