---
title: Exercise Template
menuTitle: Exercise Template
weight: 4
chapter: false
---

{{< toc >}}

---

## Sample Section Header

### Sample Subsection Header

In this page you can find a template for all the content types allowed in Learners.

## Tables

### Basic Header Formatting

| Header1: Left   | Header2: Center |  Header3: Right |
| :-------------- | :-------------: | --------------: |
| lorem ipsum ... | lorem ipsum ... | lorem ipsum ... |

### Table with Images

| Image                  | Description     |
| :--------------------- | :-------------- |
| ![alt text](image.PNG) | lorem ipsum ... |

### Layout Table Options

| {{< layout-table ratio="50 50" striped="true" divider="true" padding="20px 40px 20px 0px" >}} |                 |
| :-------------------------------------------------------------------------------------------- | :-------------- |
| ![alt text](image.PNG)                                                                        | lorem ipsum ... |
| ![alt text](image.PNG)                                                                        | lorem ipsum ... |

## Images and Figures

### No Caption

![alt text](image2.PNG)

### Caption

![This is a Figure](image2.PNG#figure)

## Exercise Forms

The exercise form will record the participants' answers and allow their answers submission. Each form is a combination of several different input types.

{{% form name="Exercise Template" %}}

{{% input-group title="Table Input Group" %}}

{{% input-table autoextend=true %}}
| Header1: Left   |         Header2: Center          |   Header3: Right |
| :-------------- | :------------------------------: | ---------------: |
| lorem ipsum ... | lorem ipsum ...                  |  lorem ipsum ... |
| lorem ipsum ... |                                  |                  |
{{% /input-table %}}

{{% input-table %}}
| Header1: Left   |         Header2: Center          |   Header3: Right |
| :-------------- | :------------------------------: | ---------------: |
|                 | lorem ipsum ...                  |  lorem ipsum ... |
| lorem ipsum ... |                                  | lorem ipsum ...  |
{{% /input-table %}}

{{% /input-group %}}

{{% input-group title="Example Input Group" extendable="true" min="0" %}}

{{< input-text
    label="Required input field with instructor information:"
    wide=true
    required=true
    placeholder="Please enter the answer"
    instructor="Here is the note for the instructor"
>}}

{{< input-text
    label="Optional input field without instructor information:"
    wide=true
    required=false
    placeholder="Please enter the answer"
>}}

{{< input-textarea
    label="Text area:"
    required=false
    placeholder="Please enter the answer"
>}} <!-- Same options of the input-text apply-->

{{< input-radio
    label="Example Radio Select"
    options="Strongly Agree (5); Agree (4); Neither Agree nor Disagree (3); Disagree (2); Strongly Disagree (1)"
    wide=true >}}

{{< input-checkboxes
    label="Example Checkbox Select"
    options="Strongly Agree (5); Agree (4); Neither Agree nor Disagree (3); Disagree (2); Strongly Disagree (1)"
    wide=true >}}

{{< input-select label="Drop-down menu:" options="Option 1; Option 2; Option 3" >}} <!-- Same options of the input-text apply-->

{{< input-file label="File Uploader" required=false >}}

{{< input-risk >}} <!-- Very specific type of input to calculate risk based on likelihood and impact -->

{{% /input-group %}}

## draw.io plugin

{{< input-group title="Incident Timeline" >}}

Use the template that is shown below to construct a timeline of the incident that is characterized by the IoCs that you have identified. To do so, click on the Edit in DrawIO button to open a new browser tab with a pre-prepared diagram that can be used to complete this exercise. When you have finished, paste the URL for the diagram into the submission box below by choosing File, Publish, Link..., Create, and then copying the generated URL.

{{< drawio src="empty_drawio.svg" >}}

{{% /input-group %}}

{{% /form %}}

{{< downloadPDF >}}  <!-- This allows the participant to download the page -->
{{< input-comment >}} <!-- This creates a feedback form for the participants -->
